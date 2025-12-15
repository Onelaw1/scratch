from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import random
import math
from ..models import User, PerformanceReview
from .. import models

class FairnessService:
    """
    Analytics for DEI (Diversity, Equity, Inclusion) and Compensation Fairness.
    """

    def analyze_fairness(self, db: Session) -> Dict[str, Any]:
        users = db.query(User).all()
        
        # 1. Prepare Data (Augment with Mocks if needed)
        data_points = []
        today = date.today()
        
        male_salaries = []
        female_salaries = []
        
        age_salary_points = [] # (Age, Salary)
        tenure_salary_points = [] # (Tenure, Salary)
        
        outliers = []
        
        for user in users:
            # Mock Demographics if missing for Demo
            gender = user.gender if user.gender else random.choice(["Male", "Female"])
            
            age = 30
            if user.birth_date:
                age = today.year - user.birth_date.year
            else:
                age = random.randint(25, 55)
                
            tenure = 1
            if user.hire_date:
                tenure = today.year - user.hire_date.year
            else:
                tenure = random.randint(1, 15)
                
            salary = user.current_salary if user.current_salary else 50000000
            
            # Mock Performance Score (1-5)
            # In real app, fetch from PerformanceReview
            perf_score = 3.0
            if user.reviews:
                # Average of review scores
                scores = [r.final_score for r in user.reviews if r.final_score]
                if scores: 
                    perf_score = sum(scores) / len(scores)
            else:
                perf_score = random.uniform(2.5, 4.8)
            
            data_points.append({
                "name": user.name,
                "gender": gender,
                "age": age,
                "tenure": tenure,
                "salary": salary,
                "performance": perf_score
            })
            
            if gender == "Male": male_salaries.append(salary)
            else: female_salaries.append(salary)
            
            age_salary_points.append((age, salary))
            
            # Outlier Detection:
            # High Performer (> 4.0) but Low Salary (< Avg - 20%) -> Risk
            # Ignoring precise distribution stats for speed, using simple thresholds
            # Assuming market avg ~ 60M
            if perf_score >= 4.0 and salary < 45000000:
                outliers.append({
                    "name": user.name,
                    "issue": "Underpaid High Performer",
                    "details": f"Score: {perf_score:.1f}, Salary: {salary/10000:.0f}만원"
                })
        
        # 2. Key Metrics
        
        # Avg Salary
        avg_male = sum(male_salaries) / len(male_salaries) if male_salaries else 0
        avg_female = sum(female_salaries) / len(female_salaries) if female_salaries else 0
        
        # Pay Gap (%) = (Male - Female) / Male
        pay_gap_pct = 0.0
        if avg_male > 0:
            pay_gap_pct = ((avg_male - avg_female) / avg_male) * 100
            
        # Age Correlation (Pearson R)
        age_corr = self.calculate_correlation(age_salary_points)
        
        return {
            "metrics": {
                "gender_pay_gap_pct": round(pay_gap_pct, 2),
                "avg_salary_male": round(avg_male),
                "avg_salary_female": round(avg_female),
                "age_pay_correlation": round(age_corr, 2), # If closer to 0, it means "Job" matters more than "Age" (Good for Job-Based)
                "total_employees": len(users)
            },
            "distributions": {
                "male_salaries": male_salaries,
                "female_salaries": female_salaries
            },
            "outliers": outliers
        }

    def calculate_correlation(self, points: List[tuple]) -> float:
        n = len(points)
        if n < 2: return 0.0
        
        sum_x = sum(p[0] for p in points)
        sum_y = sum(p[1] for p in points)
        sum_xy = sum(p[0] * p[1] for p in points)
        sum_x2 = sum(p[0] ** 2 for p in points)
        sum_y2 = sum(p[1] ** 2 for p in points)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
        
        if denominator == 0: return 0.0
        return numerator / denominator

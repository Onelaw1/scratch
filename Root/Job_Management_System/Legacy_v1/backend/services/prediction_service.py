from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import date
import random
from ..models import User

class PredictionService:
    """
    AI-driven Predictive Analytics for HR.
    Focus: Attrition (Flight Risk) Prediction.
    """

    def predict_attrition(self, db: Session) -> Dict[str, Any]:
        users = db.query(User).all()
        today = date.today()
        
        high_risk_employees = []
        department_risks = {}
        
        for user in users:
            # 1. Feature Extraction (Mocking missing data for robust demo)
            
            # Tenure (Years)
            tenure = 0
            if user.hire_date:
                tenure = today.year - user.hire_date.year
            else:
                tenure = random.randint(1, 15)
                
            # Current Salary vs Market (Simple Heuristic for Demo)
            salary = user.current_salary if user.current_salary else 50000000
            market_rate_approx = 60000000 # Assume average
            pay_gap_pct = (market_rate_approx - salary) / market_rate_approx
            
            # Pulse Survey Score (Mock Stress: 1-10)
            # In real system, fetch from PulseSurvey table
            stress_score = random.randint(3, 9) 
            
            # Performance (Mock: 1-5)
            perf_score = random.uniform(2.5, 4.8)
            
            # 2. Risk Calculation Algorithm (The "AI" Model)
            risk_score = 0
            reasons = []
            
            # Factor A: Salary (Weight: 30%)
            if pay_gap_pct > 0.1: # 10% underpaid
                risk_score += 30
                reasons.append("Underpaid vs Market")
            elif pay_gap_pct > 0.2: # 20% underpaid
                risk_score += 50
                reasons.append("Significantly Underpaid")
                
            # Factor B: Stress (Weight: 30%)
            if stress_score >= 8:
                risk_score += 30
                reasons.append("High Burnout Risk")
                
            # Factor C: The "Itch" Year (3-4 years tenure) (Weight: 20%)
            if 3 <= tenure <= 5:
                risk_score += 20
                reasons.append("Career Transition Period (3-5y)")
                
            # Factor D: High Performer Mobility (Multiplier)
            if perf_score >= 4.0:
                risk_score *= 1.2 # High performers have more options
                if risk_score > 40:
                    reasons.append("High Market Employability")
            
            # Cap at 99%
            risk_score = min(risk_score, 99)
            risk_score = max(risk_score, 10) # Min 10%
            
            if risk_score >= 70:
                high_risk_employees.append({
                    "user_id": user.id,
                    "name": user.name,
                    "position": "Employee", # Placeholder
                    "risk_score": int(risk_score),
                    "factors": reasons,
                    "tenure": tenure,
                    "stress": stress_score
                })
                
        # Sort by Risk Descending
        high_risk_employees.sort(key=lambda x: x["risk_score"], reverse=True)
        
        return {
            "total_employees": len(users),
            "avg_risk_score": 42, # Mock Avg
            "high_risk_count": len(high_risk_employees),
            "high_risk_list": high_risk_employees[:10] # Top 10
        }

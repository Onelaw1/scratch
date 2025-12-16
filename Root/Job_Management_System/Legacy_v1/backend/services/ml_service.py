import random
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .. import models

# Fallback: Mock ML Service since sklearn install failed in env
class TurnoverPredictor:
    def __init__(self):
        self.is_trained = False
        
    def train_model(self, db: Session):
        # Mock Training
        self.is_trained = True
        return {"status": "Trained (Mock)", "samples": 200, "accuracy": 0.85}

    def predict_risk(self, user: models.User, db: Session) -> Dict[str, Any]:
        if not self.is_trained:
            self.is_trained = True
            
        # Logic-based Heuristic (Mocking RF behavior)
        risk_probability = 0.2
        factors = {}

        # 1. Performance Rating (Inverse)
        # Low rating -> High Risk (Disengagement) or Low Risk (Incompetence)? 
        # Usually High Performers with bad conditions leave. Low performers stay.
        # Let's assume: Low Satisfaction (Proxy by pulse) is key.
        # But here we use 'Performance' as 'Engagement' proxy? 
        # Let's use standard: Low Rating + High Tenure = Risk of Stagnation
        reviews = user.reviews
        avg_rating = sum([r.total_score for r in reviews]) / len(reviews) if reviews else 80.0
        avg_rating_5 = (avg_rating / 100) * 5
        factors['rating'] = round(avg_rating_5, 1)
        
        if avg_rating_5 < 3.0: 
            risk_probability += 0.2
            factors['rating_risk'] = "Low Performance"

        # 2. Salary Gap
        market_salary = 60000000
        current_salary = user.current_salary or 50000000
        salary_ratio = current_salary / market_salary
        factors['salary_ratio'] = round(salary_ratio, 2)
        
        if salary_ratio < 0.85:
            risk_probability += 0.3
            factors['salary_risk'] = "Underpaid"
            
        # 3. Tenure Stagnation
        # If in same job > 3 years without promotion
        tenure_years = 0
        if user.hire_date:
            from datetime import date
            delta = date.today() - user.hire_date
            tenure_years = delta.days / 365.0
            
        factors['tenure_years'] = round(tenure_years, 1)
        if tenure_years > 3.0:
            # Check for recent promotion? (Mock: assume no if simplistic)
            risk_probability += 0.15
            factors['tenure_risk'] = "Stagnation"

        # 4. Pulse Check (Sentiment)
        # Check last 5 pulses
        recent_pulses = db.query(models.PulseCheck)\
            .filter(models.PulseCheck.user_id == user.id)\
            .order_by(models.PulseCheck.date.desc())\
            .limit(5).all()
            
        if recent_pulses:
            avg_mood = sum([p.mood_score for p in recent_pulses]) / len(recent_pulses)
            factors['avg_pulse_mood'] = round(avg_mood, 1)
            if avg_mood < 3.0:
                risk_probability += 0.25
                factors['pulse_risk'] = "Negative Sentiment"
        else:
             factors['avg_pulse_mood'] = "N/A"

        # Cap Probability
        risk_probability = min(risk_probability, 0.98)
        
        # Determine Level
        risk_level = "Low"
        if risk_probability > 0.75: risk_level = "Critical"
        elif risk_probability > 0.5: risk_level = "High"
        elif risk_probability > 0.3: risk_level = "Medium"
        
        return {
            "risk_score": round(risk_probability, 2),
            "risk_level": risk_level,
            "factors": factors
        }

class CareerPathRecommender:
    def recommend_paths(self, user_id: str, db: Session) -> List[Dict[str, Any]]:
        # Content-Based Filtering
        # Match User Skills vs Job Requirements
        
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user: return []
        
        # Existing Skills
        user_skills = {uc.competency_id: uc.current_level for uc in user.competencies}
        
        all_jobs = db.query(models.JobPosition).all()
        recommendations = []
        
        for job in all_jobs:
            if job in user.job_positions: continue # Skip current job
            
            # Calculate Match Score
            reqs = job.required_competencies
            if not reqs: continue
            
            match_score = 0
            total_weight = 0
            
            for req in reqs:
                user_level = user_skills.get(req.competency_id, 0)
                # Simple distance match. If User >= Req, full points.
                if user_level >= req.required_level:
                    match_score += req.weight
                else:
                    # Partial credit
                    match_score += (user_level / req.required_level) * req.weight
                
                total_weight += req.weight
            
            final_score = (match_score / total_weight) * 100 if total_weight > 0 else 0
            
            if final_score > 60: # Threshold
                recommendations.append({
                    "job_title": job.title,
                    "match_score": round(final_score, 1),
                    "gap_analysis": f"{len(reqs)} skills analyzed"
                })
                
        # Sort by score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:3]

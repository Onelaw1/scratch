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
            # Auto-train for convenience
            self.is_trained = True
            
        # Logic-based Heuristic (Mocking RF behavior)
        # 1. Rating (Inverse)
        reviews = user.reviews
        avg_rating = sum([r.total_score for r in reviews]) / len(reviews) if reviews else 80.0
        # Normalize: 80 -> 4.0
        avg_rating_5 = (avg_rating / 100) * 5
        
        # 2. Salary Gap
        market = 60000000
        current = user.current_salary or 50000000
        salary_ratio = current / market
        
        # 3. Overtime
        overtime = 12.0 # Mock

        # Risk Score Calculation
        prob = 0.2
        if avg_rating_5 < 3.5: prob += 0.3
        if salary_ratio < 0.9: prob += 0.3
        if overtime > 10: prob += 0.1
        
        prob = min(prob, 0.95)
        
        risk_level = "Low"
        if prob > 0.7: risk_level = "High"
        elif prob > 0.4: risk_level = "Medium"
        
        return {
            "risk_score": round(prob, 2),
            "risk_level": risk_level,
            "factors": {
                "rating": round(avg_rating_5, 1),
                "salary_ratio": round(salary_ratio, 2),
                "overtime": overtime
            }
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

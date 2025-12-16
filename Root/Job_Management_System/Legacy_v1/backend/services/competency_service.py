from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models

class CompetencyService:
    def __init__(self, db: Session):
        self.db = db

    def analyze_fit(self, user_id: str) -> Dict[str, Any]:
        """
        Analyzes Job-Person Competency Fit.
        Compares Job Requirements (Standard) vs User Skills (Actual).
        """
        
        # 1. Fetch User & Current Job
        # Assuming user has at least one job position assigned or we pick the latest
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
             return {"error": "User not found"}
             
        job_pos = None
        if user.job_positions:
            # Take the most recent one or the first one
            job_pos = user.job_positions[0] 
        
        user_name = user.name
        job_title = job_pos.title if job_pos else "No Position Assigned"
        
        # 2. Fetch Requirements (JobCompetency)
        required_skills = []
        if job_pos:
            job_comps = self.db.query(models.JobCompetency).filter(models.JobCompetency.job_position_id == job_pos.id).all()
            for jc in job_comps:
                required_skills.append({
                    "id": jc.competency.id,
                    "name": jc.competency.name,
                    "required_level": jc.required_level,
                    "description": jc.competency.description
                })
        
        # If no requirements, we can't analyze fit properly, but let's proceed empty
        
        # 3. Fetch Actual Skills (UserCompetency)
        actual_skills_map = {}
        user_comps = self.db.query(models.UserCompetency).filter(models.UserCompetency.user_id == user_id).all()
        for uc in user_comps:
            actual_skills_map[uc.competency_id] = uc.current_level
            
        # 4. Calculate Fit & Radar Data
        radar_data = []
        gaps = []
        strengths = []
        
        total_req_points = 0
        total_act_points = 0
        
        for req in required_skills:
            req_lvl = req["required_level"]
            act_lvl = actual_skills_map.get(req["id"], 0) # Default to 0 if missing
            
            diff = act_lvl - req_lvl
            
            radar_data.append({
                "skill": req["name"],
                "required": req_lvl,
                "actual": act_lvl,
                "fullMark": 5
            })
            
            total_req_points += req_lvl
            total_act_points += act_lvl
            
            if diff < 0:
                gaps.append({
                    "skill": req["name"],
                    "gap": diff,
                    "action": "Training Required" if diff >= -1 else "Urgent Coaching"
                })
            elif diff > 0:
                strengths.append({
                    "skill": req["name"],
                    "surplus": diff,
                    "action": "Mentor Potential"
                })
                
        # Handle case where user has skills NOT in job reqs? (Optional, maybe show as extra strengths)
        
        # Fit Score
        fit_score = 0.0
        if total_req_points > 0:
            # Capped at 100%? Or allow > 100? Typically fit is how well they meet reqs.
            # If act > req, it's 100% met.
            # Let's do a simple ratio but cap the contribution of each skill to the required level?
            # For this simple version, simple ratio but maybe cap total?
            fit_score = (total_act_points / total_req_points) * 100
            fit_score = min(round(fit_score, 1), 100.0)
        elif not required_skills and user_comps:
             fit_score = 100.0 # No reqs, but has skills?
        
        return {
            "analyzed_at": datetime.now().strftime("%Y-%m-%d"),
            "user_id": user_id,
            "user_name": user_name,
            "job_title": job_title,
            "fit_score": fit_score,
            "radar_data": radar_data,
            "analysis": {
                "gaps": gaps,
                "strengths": strengths
            }
        }

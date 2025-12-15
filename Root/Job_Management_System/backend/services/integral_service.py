from typing import List, Dict, Any
from sqlalchemy.orm import Session
import random
from datetime import datetime
from ..models import User

class IntegralService:
    """
    Scientific Performance Analysis.
    Calculates "Achievement Integral" (Area under the Performance Curve).
    """

    def calculate_integral(self, db: Session, user_id: str) -> Dict[str, Any]:
        # For this demo, we will generate synthetic historical data 
        # because our mock database doesn't have 5 years of history.
        
        current_year = datetime.now().year
        history = []
        cumulative_score = 0.0
        years = 5
        
        # Determine "Persona" (Consistency Type) based on simple hash of user_id
        # ensuring consistent results for the same user
        random.seed(user_id)
        persona_type = random.choice(["CONSISTENT_HIGH", "RISING_STAR", "ERRATIC", "STAGNANT"])
        
        base_score = 0
        if persona_type == "CONSISTENT_HIGH": base_score = 4.2
        elif persona_type == "RISING_STAR": base_score = 3.0
        elif persona_type == "ERRATIC": base_score = 3.5
        else: base_score = 2.8
        
        for i in range(years):
            year = current_year - (years - 1 - i)
            
            # Fluctuate based on persona
            score = 0.0
            if persona_type == "CONSISTENT_HIGH":
                score = base_score + random.uniform(-0.2, 0.3)
            elif persona_type == "RISING_STAR":
                score = base_score + (i * 0.4) + random.uniform(-0.1, 0.2) # Upward slope
            elif persona_type == "ERRATIC":
                score = base_score + random.uniform(-1.0, 1.0)
            else:
                score = base_score + random.uniform(-0.1, 0.1)
                
            # Cap at 5.0
            score = min(score, 5.0)
            score = max(score, 1.0)
            
            cumulative_score += score
            
            grade = "B"
            if score >= 4.5: grade = "S"
            elif score >= 4.0: grade = "A"
            elif score >= 3.0: grade = "B"
            elif score >= 2.0: grade = "C"
            else: grade = "D"
            
            history.append({
                "year": year,
                "score": round(score, 2),
                "grade": grade,
                "cumulative": round(cumulative_score, 2)
            })
            
        # Calculate derived metrics
        avg_score = cumulative_score / years
        consistency_index = 0.0 # Standard Deviation would go here
        
        return {
            "user_id": user_id,
            "persona": persona_type,
            "total_integral": round(cumulative_score, 2), # The "Area"
            "avg_score": round(avg_score, 2),
            "history": history
        }

    def get_all_integrals(self, db: Session) -> Dict[str, Any]:
        users = db.query(User).all()
        results = []
        for user in users:
            data = self.calculate_integral(db, user.id)
            data["name"] = user.name
            data["position"] = user.position.title if user.position else "Employee"
            results.append(data)
            
        # Sort by Total Integral Descending
        results.sort(key=lambda x: x["total_integral"], reverse=True)
        
        return {
            "count": len(users),
            "top_performers": results[:10],
            "analysis_date": datetime.now().isoformat()
        }

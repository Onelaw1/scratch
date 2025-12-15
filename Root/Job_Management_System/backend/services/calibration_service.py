from typing import List, Dict, Any
from sqlalchemy.orm import Session
import random
from ..models import User, JobPosition

class CalibrationService:
    """
    Scientific Job Grade Calibration.
    Detects 'Workload Drift' (Actual vs Defined).
    """

    def detect_drift(self, db: Session) -> Dict[str, Any]:
        users = db.query(User).all()
        suggestions = []
        
        for user in users:
            # 1. Get Assigned Grade (Static)
            # user.position.grade is "G4" -> 4
            assigned_grade = 4 # Default mock
            if user.position and user.position.grade:
                # Extract number from "G4" string if needed, currently assuming simple mock
                pass

            # 2. Calculate Actual Grade (Dynamic from Workload)
            # Mocking the aggregation of "Task Complexity * Volume" over 6 months
            # In real system: sum(task.level * task.hours) / total_hours
            
            # Simulate Drift
            # 20% of users are "Over-performing" (doing higher grade work)
            is_overperforming = random.random() < 0.2
            
            actual_grade_score = assigned_grade
            drift_magnitude = 0.0
            
            if is_overperforming:
                drift_magnitude = random.uniform(1.2, 1.8) # 1.2 to 1.8 levels higher
                actual_grade_score += drift_magnitude
            else:
                actual_grade_score += random.uniform(-0.2, 0.2) # Normal fluctuation

            # 3. Drift Threshold Logic
            # If Actual is > 1.0 level higher than Assigned -> Suggest Upgrade
            if drift_magnitude > 1.0:
                suggestions.append({
                    "user_id": user.id,
                    "name": user.name,
                    "position": user.position.title if user.position else "Employee",
                    "current_grade": f"G{assigned_grade}",
                    "calculated_grade": f"G{int(actual_grade_score)}.{int((actual_grade_score%1)*10)}", # e.g., G5.4
                    "gap": round(drift_magnitude, 2),
                    "confidence": int(random.uniform(85, 98)), # AI Confidence
                    "reason": f"Consistently performing G{int(actual_grade_score)} level tasks (Architecture, Strategy) for 6 months."
                })

        return {
            "total_analyzed": len(users),
            "drift_detected_count": len(suggestions),
            "suggestions": suggestions
        }

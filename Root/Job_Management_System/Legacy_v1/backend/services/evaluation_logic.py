from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
from collections import defaultdict
import math

class EvaluationLogicService:
    @staticmethod
    def get_assignment(db: Session, session_id: str, rater_user_id: str, target_job_id: str):
        return db.query(models.EvaluationAssignment).filter(
            models.EvaluationAssignment.session_id == session_id,
            models.EvaluationAssignment.rater_user_id == rater_user_id,
            models.EvaluationAssignment.target_job_position_id == target_job_id
        ).first()

    @staticmethod
    def get_my_assignments(db: Session, session_id: str, rater_user_id: str):
        return db.query(models.EvaluationAssignment).filter(
            models.EvaluationAssignment.session_id == session_id,
            models.EvaluationAssignment.rater_user_id == rater_user_id
        ).all()

    @staticmethod
    def validate_evaluation_access(db: Session, session_id: str, rater_user_id: str, target_job_id: str) -> bool:
        # Strict Mode: Must have assignment
        assignment = EvaluationLogicService.get_assignment(db, session_id, rater_user_id, target_job_id)
        if assignment:
            return True
        return False

    @staticmethod
    def analyze_rater_bias(db: Session, session_id: str, rater_user_id: str, new_ratings: list = None):
        """
        Analyzes bias based on A/B Comparison:
        - Before: Existing DB scores
        - After: Existing DB scores + new_ratings (merged)
        """
        # 1. Fetch existing committed scores (Before State)
        existing_scores = db.query(models.JobEvaluationScore).join(models.JobEvaluation).filter(
            models.JobEvaluation.session_id == session_id,
            models.JobEvaluationScore.rater_user_id == rater_user_id
        ).all()
        
        # Map: { job_id: factor_scores_dict }
        before_state = {}
        for s in existing_scores:
            before_state[s.evaluation.job_position_id] = s.factor_scores

        # 2. Build After State (Merge New)
        after_state = before_state.copy()
        if new_ratings:
            for r in new_ratings:
                # Support both Pydantic model and dict
                job_id = r.job_position_id if hasattr(r, 'job_position_id') else r['job_position_id']
                f_scores = r.factor_scores if hasattr(r, 'factor_scores') else r['factor_scores']
                after_state[job_id] = f_scores

        # Helper: Calculate Stats
        def calculate_stats(state_map):
            if not state_map:
                return {"count": 0, "average": 0.0, "distribution": {}}
            
            averages = []
            for f_scores in state_map.values():
                if not f_scores: continue
                vals = list(f_scores.values())
                if vals:
                    averages.append(sum(vals) / len(vals))
            
            if not averages:
                return {"count": 0, "average": 0.0, "distribution": {}}
                
            total_avg = sum(averages) / len(averages)
            
            # Distribution
            dist = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}
            for val in averages:
                if val <= 2: dist["0-2"] += 1
                elif val <= 4: dist["2-4"] += 1
                elif val <= 6: dist["4-6"] += 1
                elif val <= 8: dist["6-8"] += 1
                else: dist["8-10"] += 1
                
            return {
                "count": len(averages),
                "average": round(total_avg, 2),
                "distribution": dist
            }

        stats_before = calculate_stats(before_state)
        stats_after = calculate_stats(after_state)
        
        # Bias Warning based on AFTER state
        avg = stats_after["average"]
        warning = "Balanced"
        if avg > 8.0: warning = "High Leniency"
        elif avg < 4.0: warning = "High Strictness"

        return {
            "before": stats_before,
            "after": stats_after,
            "bias_warning": warning
        }

import random
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import JobPosition, JobTask, User

class DynamicJDService:
    def __init__(self, db: Session):
        self.db = db

    def analyze_job_drift(self, job_id: str) -> Dict[str, Any]:
        """
        Analyzes the "Drift" between the Job Description (Theory) and Workload Logs (Reality).
        Returns suggestions to Add or Remove tasks.
        """
        # 1. Fetch Job Definitions (Theory)
        # For simulation, we might not have a real job_id in the DB, so we simulate.
        # job = self.db.query(JobPosition).filter(JobPosition.id == job_id).first()
        
        # Simulate "Theory" (Current JD)
        current_jd_tasks = [
            {"id": "t1", "category": "Planning", "task_name": "Strategic Planning"},
            {"id": "t2", "category": "Reporting", "task_name": "Monthly Report"},
            {"id": "t3", "category": "Management", "task_name": "Team Meeting"},
            {"id": "t4", "category": "Sales", "task_name": "Client Call"}, # Obsolete candidate
        ]

        # Simulate "Reality" (Workload Logs from last 90 days)
        # We find tasks that are logged frequently.
        # In a real scenario, we would query WorkloadLog grouped by task_category/description.
        
        # Scenario: User is doing "Data Analysis" (New) and not doing "Client Call" (Obsolete)
        reality_tasks = [
            {"name": "Strategic Planning", "frequency": "High", "match": "t1"},
            {"name": "Monthly Report", "frequency": "Medium", "match": "t2"},
            {"name": "Team Meeting", "frequency": "High", "match": "t3"},
            {"name": "Data Analysis", "frequency": "High", "match": None}, # NO MATCH -> NEW
            {"name": "AI Model Tuning", "frequency": "Medium", "match": None}, # NO MATCH -> NEW
        ]

        # 2. Detect Drift
        new_task_suggestions = []
        obsolete_task_suggestions = []

        # Find New Tasks (In Reality, Not in JD)
        for real_task in reality_tasks:
            if real_task["match"] is None:
                new_task_suggestions.append({
                    "task_name": real_task["name"],
                    "reason": f"Logged frequently ({real_task['frequency']}) in last 90 days.",
                    "confidence": 95 if real_task['frequency'] == 'High' else 70
                })

        # Find Obsolete Tasks (In JD, Not in Reality)
        reality_task_names = [t["name"] for t in reality_tasks] # Simplified matching logic
        # Ideally match by ID, but for simulation we assume if 'match' refers to ID.
        matched_ids = [t["match"] for t in reality_tasks if t["match"]]

        for jd_task in current_jd_tasks:
            if jd_task["id"] not in matched_ids:
                obsolete_task_suggestions.append({
                    "task_id": jd_task["id"],
                    "task_name": jd_task["task_name"],
                    "reason": "No logs found in last 90 days.",
                    "confidence": 85
                })

        drift_score = len(new_task_suggestions) + len(obsolete_task_suggestions)
        status = "high_drift" if drift_score >= 2 else "stable"

        return {
            "job_id": job_id,
            "job_title": "Marketing Manager", # Mock
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "drift_score": drift_score,
            "status": status,
            "current_jd_summary": [t["task_name"] for t in current_jd_tasks],
            "suggestions": {
                "add": new_task_suggestions,
                "remove": obsolete_task_suggestions
            }
        }

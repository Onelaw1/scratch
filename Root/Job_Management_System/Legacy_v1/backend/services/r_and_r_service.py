from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

class RAndRService:
    def __init__(self, db: Session):
        self.db = db

    def analyze_conflicts(self) -> Dict[str, Any]:
        """
        Analyzes R&R conflicts (Duplications and Gaps).
        Returns a matrix of Department vs Task Category.
        """
        # 1. Simulate Workload Data by Department
        # In reality, this would query WorkloadLog joined with User and OrgUnit
        
        departments = ["Sales Team", "Marketing Team", "Engineering Team", "HR Manager"]
        categories = ["Market Research", "Recruiting", "System Dev", "Data Privacy"]

        # Simulated Volume (Task Count / Intensity)
        matrix = {
            "Market Research": {"Sales Team": 30, "Marketing Team": 40, "Engineering Team": 0, "HR Manager": 0},
            "Recruiting": {"Sales Team": 15, "Marketing Team": 0, "Engineering Team": 0, "HR Manager": 12},
            "System Dev": {"Sales Team": 0, "Marketing Team": 5, "Engineering Team": 90, "HR Manager": 0},
            "Data Privacy": {"Sales Team": 0, "Marketing Team": 0, "Engineering Team": 0, "HR Manager": 0}, # GAP!
        }

        # 2. Detect Conflicts
        duplications = []
        gaps = []

        for category, dept_data in matrix.items():
            active_depts = [dept for dept, vol in dept_data.items() if vol > 10] # Threshold > 10
            
            # Duplication Logic: More than 1 dept doing significant work
            if len(active_depts) >= 2:
                duplications.append({
                    "category": category,
                    "involved_depts": active_depts,
                    "reason": "Multiple departments performing significant volume.",
                    "severity": "High"
                })

            # Gap Logic: No dept doing the work (Total volume near 0)
            total_vol = sum(dept_data.values())
            if total_vol < 5:
                gaps.append({
                    "category": category,
                    "reason": "Critical function with essentially zero volume.",
                    "severity": "Critical"
                })

        return {
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "matrix": matrix,
            "departments": departments,
            "categories": categories,
            "alerts": {
                "duplications": duplications,
                "gaps": gaps
            }
        }

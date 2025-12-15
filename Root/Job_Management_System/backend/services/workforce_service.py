import random
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import User, JobPosition

class WorkforceService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_optimal_headcount(self) -> Dict[str, Any]:
        """
        Calculates Scientific Optimal Workforce (Required FTE) for each department.
        Formula: (Standard Time * Monthly Volume) / (Working Hours * Utilization Rate)
        """
        departments = ["Sales", "Engineering", "HR", "Finance", "Marketing", "Operations"]
        results = []

        total_gap = 0.0

        for dept_name in departments:
            # Simulate Data for each Department
            current_fte = random.randint(3, 15)  # Current headcount
            
            # Variables for Formula
            # 1. Total Transaction Vol: e.g. 5000 tickets, 200 commits, 50 reports
            monthly_volume = random.randint(100, 5000) 
            
            # 2. Avg Standard Time per Unit (minutes): e.g. 30 mins
            avg_standard_time_mins = random.uniform(10.0, 120.0) 
            
            # 3. Target Utilization (Effective Working Ratio): 0.85 (85%)
            target_utilization = 0.85
            
            # 4. Monthly Working Minutes: 160 hours * 60 = 9600 mins
            monthly_working_mins = 160 * 60 

            # Calculation: Total Workload (mins)
            total_workload_mins = monthly_volume * avg_standard_time_mins
            
            # Application of Formula
            # Required FTE = Total Workload / (Working Time * Utilization)
            required_fte = total_workload_mins / (monthly_working_mins * target_utilization)
            
            # Productivity Index (Required / Current)
            # > 1.0 : Overworked (Need more people)
            # < 1.0 : Idle (Process inefficient or overstaffed)
            productivity_index = required_fte / current_fte if current_fte > 0 else 0

            gap = required_fte - current_fte
            total_gap += gap

            status = "Optimal"
            if productivity_index > 1.2:
                status = "Overworked (Critical)"
            elif productivity_index > 1.1:
                status = "Overworked (Warning)"
            elif productivity_index < 0.7:
                status = "Idle (Inefficient)"
            
            results.append({
                "department": dept_name,
                "current_fte": current_fte,
                "required_fte": round(required_fte, 1),
                "gap": round(gap, 1),
                "productivity_index": round(productivity_index * 100, 1), # Percentage
                "monthly_volume": monthly_volume,
                "avg_process_time": round(avg_standard_time_mins, 1),
                "status": status
            })

        # Sort by greatest shortage first
        results.sort(key=lambda x: x["gap"], reverse=True)

        return {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula": "FTE = (Vol x Time) / (160h x 0.85)",
            "total_hiring_need": round(total_gap, 1) if total_gap > 0 else 0,
            "department_analysis": results
        }

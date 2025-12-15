from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

class RACIService:
    def __init__(self, db: Session):
        self.db = db

    def generate_raci_matrix(self, process_id: str) -> Dict[str, Any]:
        """
        Auto-generates a RACI Matrix for a given Business Process.
        Infers roles based on theoretical logic (for simulation).
        """
        # Mock Data Simulation
        process_name = "Recruiting Process" if process_id == "hiring" else "Budget Planning"
        
        # 1. Define Steps in the Process
        steps = [
            {"id": "s1", "name": "Define Job Req", "category": "Planning"},
            {"id": "s2", "name": "Screen Resumes", "category": "Execution"},
            {"id": "s3", "name": "Interview Candidates", "category": "Execution"},
            {"id": "s4", "name": "Final Offer Approval", "category": "Decision"},
            {"id": "s5", "name": "Onboarding Setup", "category": "Admin"},
        ]

        # 2. Define Stakeholders (Roles/Depts)
        stakeholders = ["Hiring Manager", "Recruiter (HR)", "HR Director", "Finance Team", "IT Team"]

        # 3. Auto-Assign RACI (Simulation Logic)
        # R = Responsible (Doer), A = Accountable (Approver), C = Consulted, I = Informed
        raci_matrix = []

        for step in steps:
            row = {"step": step["name"], "roles": {}}
            
            if step["category"] == "Planning":
                row["roles"]["Hiring Manager"] = "R"
                row["roles"]["Recruiter (HR)"] = "C"
                row["roles"]["HR Director"] = "A"
                row["roles"]["Finance Team"] = "I" # Budget check
                row["roles"]["IT Team"] = ""

            elif step["category"] == "Execution":
                # Screening / Interview
                row["roles"]["Hiring Manager"] = "C"
                row["roles"]["Recruiter (HR)"] = "R"
                row["roles"]["HR Director"] = "I"
                row["roles"]["Finance Team"] = ""
                row["roles"]["IT Team"] = ""
            
            elif step["category"] == "Decision":
                # Final Offer
                row["roles"]["Hiring Manager"] = "C"
                row["roles"]["Recruiter (HR)"] = "R" # Prepares offer
                row["roles"]["HR Director"] = "A" # Signs off
                row["roles"]["Finance Team"] = "C" # Salary check
                row["roles"]["IT Team"] = ""
            
            elif step["category"] == "Admin":
                # Onboarding
                row["roles"]["Hiring Manager"] = "I"
                row["roles"]["Recruiter (HR)"] = "A"
                row["roles"]["HR Director"] = ""
                row["roles"]["Finance Team"] = ""
                row["roles"]["IT Team"] = "R" # Setup laptop

            raci_matrix.append(row)

        return {
            "process_id": process_id,
            "process_name": process_name,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stakeholders": stakeholders,
            "matrix": raci_matrix
        }

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import JobDescription

class NCSComplianceService:
    """
    Auto-Audit Engine for NCS Compliance.
    Compares internal JDs against Government Standards.
    """

    # Mock NCS Database (Government Standards)
    # In reality, this would be a massive DB or API call to ncs.go.kr
    NCS_STANDARDS = {
        "02020201": { # IT Project Management
            "name": "IT Project Management",
            "keywords": ["Risk Management", "Schedule Planning", "Stakeholder Analysis", "Budgeting", "Quality Assurance", "WBS"],
            "core_competencies": ["Strategic Thinking", "Communication", "Public Ethics"]
        },
        "02010101": { # General Administration
            "name": "General Administration",
            "keywords": ["Document Management", "Meeting Minutes", "Asset Management", "Procurement", "Customer Service"],
            "core_competencies": ["Public Ethics", "Problem Solving", "Resource Management"]
        },
        "09010101": { # Data Analysis (Mock Code)
            "name": "Big Data Analysis",
            "keywords": ["Python", "SQL", "Machine Learning", "Statistical Analysis", "Data Visualization", "ETL"],
            "core_competencies": ["Mathematical Reasoning", "Information Literacy", "Technology Application"]
        }
    }

    def audit_job_description(self, job_desc: JobDescription, ncs_code: str = None) -> Dict[str, Any]:
        """
        Audits a single JD against NCS Standards.
        """
        # 1. Identify Target NCS Standard
        # Simple heuristic: If no code provided, try to match by Job Name substring
        target_standard = None
        target_code = ncs_code
        
        if not target_code:
            # Auto-Detection Logic (Mock)
            job_title = job_desc.title.lower() if job_desc.title else ""
            if "data" in job_title or "scientist" in job_title: target_code = "09010101"
            elif "project" in job_title or "manager" in job_title: target_code = "02020201"
            else: target_code = "02010101" # Default to Admin
            
        target_standard = self.NCS_STANDARDS.get(target_code)
        
        if not target_standard:
            return {"status": "ERROR", "message": "NCS Standard not found"}

        # 2. Text Analysis (Keyword Matching)
        # Combine JD content for search
        jd_text = (job_desc.summary or "") + " " + " ".join(job_desc.responsibilities or []) + " " + " ".join(job_desc.skills or [])
        jd_text = jd_text.lower()
        
        matched_keywords = []
        missing_keywords = []
        
        for kw in target_standard["keywords"]:
            if kw.lower() in jd_text:
                matched_keywords.append(kw)
            else:
                missing_keywords.append(kw)
                
        # 3. Calculate Score
        total_items = len(target_standard["keywords"])
        match_count = len(matched_keywords)
        score = int((match_count / total_items) * 100) if total_items > 0 else 0
        
        # 4. Generate Report
        grade = "C"
        if score >= 80: grade = "A"
        elif score >= 60: grade = "B"
        
        return {
            "status": "SUCCESS",
            "job_id": job_desc.job_id,
            "job_title": job_desc.title,
            "ncs_standard": target_standard["name"],
            "ncs_code": target_code,
            "compliance_score": score,
            "grade": grade,
            "matched_items": matched_keywords,
            "missing_items": missing_keywords,
            "core_competencies_check": "Pass" if score > 50 else "Requires Review" # Simplified logic
        }

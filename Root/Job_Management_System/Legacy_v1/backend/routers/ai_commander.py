from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db
# In a real scenario, this would import LangChain or similar
import random

router = APIRouter(
    prefix="/ai-commander",
    tags=["AI Architect"],
)

@router.post("/architect/job", response_model=dict)
def architect_job(
    request: dict, # { "title": "Safety Manager", "ncs_code": "040101" }
    db: Session = Depends(get_db)
):
    """
    [Superior Feature] AI Job Architect
    Generates a full legal-compliant Job Description from minimal input.
    """
    title = request.get("title")
    ncs_code = request.get("ncs_code")
    
    # 1. Mock AI Generation Logic
    # Real logic: Query LLM with NCS data context
    ai_tasks = [
        {"name": "Establish Site Safety Plan", "importance": 5},
        {"name": "Conduct Risk Assessment", "importance": 5},
        {"name": "Training Compliance Check", "importance": 4}
    ]
    ai_reqs = [
        {"category": "Certification", "content": "Industrial Safety Engineer (Level 1)"},
        {"category": "Knowledge", "content": "Occupational Safety and Health Act"},
        {"category": "Experience", "content": "Minimum 5 years in Construction"}
    ]
    
    # 2. Create Job Record
    new_job = models.JobPosition(
        title=title,
        ncs_code_id=ncs_code, # Assuming this ID exists or created on fly
        creation_source=models.AISource.AI_GENERATED,
        ai_confidence_score=0.95,
        summary=f"AI-Generated Strategic Position for {title} aligned with NCS {ncs_code}."
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    # 3. Add Components
    for task in ai_tasks:
        db.add(models.JobTask(job_id=new_job.id, **task))
    for req in ai_reqs:
        db.add(models.JobRequirement(job_id=new_job.id, **req))
        
    # 4. Auto-Run Fairness Audit (Self-Correction)
    # Mock Violation Check
    audit_status = models.ComplianceStatus.PASS
    if "Man" in title: # Simple bias check
        audit_status = models.ComplianceStatus.WARNING
        db.add(models.FairnessAuditLog(
            target_job_id=new_job.id,
            check_type="GENDER_BIAS",
            status=audit_status,
            message="Job Title implies gender bias (Man). Suggest using 'Person' or 'Officer'."
        ))
        
    db.commit()
    
    return {
        "status": "success",
        "job_id": new_job.id,
        "ai_message": "Architected complete structure with NCS alignment.",
        "fairness_audit": audit_status
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/fairness-audit",
    tags=["Fairness Engine"],
)

@router.get("/job/{job_id}", response_model=List[schemas.FairnessAuditLog])
def get_job_audit_logs(job_id: str, db: Session = Depends(get_db)):
    """
    Get all audit logs for a specific job.
    """
    return db.query(models.FairnessAuditLog).filter(models.FairnessAuditLog.target_job_id == job_id).all()

@router.post("/run-audit/{job_id}")
def run_manual_audit(job_id: str, db: Session = Depends(get_db)):
    """
    Manually trigger the Fairness Engine on a Job.
    """
    job = db.query(models.JobPosition).filter(models.JobPosition.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Mock Audit Logic
    flags = []
    # Check 1: Title Bias
    if "Man" in job.title or "Girl" in job.title:
        flags.append({
            "check_type": "GENDER_BIAS",
            "status": models.ComplianceStatus.WARNING,
            "message": f"Potential gender bias in title: '{job.title}'"
        })
    
    # Check 2: Requirement Bias (e.g. Age)
    for req in job.requirements:
        if "Age" in req.content or "Young" in req.content:
             flags.append({
                "check_type": "AGE_BIAS",
                "status": models.ComplianceStatus.VIOLATION,
                "message": f"Age discrimination detected in requirement: '{req.content}'"
            })

    # Save Logs
    created_logs = []
    if not flags:
        # Pass Log
        log = models.FairnessAuditLog(
            target_job_id=job.id,
            check_type="GENERAL_CHECK",
            status=models.ComplianceStatus.PASS,
            message="No obvious bias detected."
        )
        db.add(log)
        created_logs.append(log)
    else:
        for flag in flags:
            log = models.FairnessAuditLog(target_job_id=job.id, **flag)
            db.add(log)
            created_logs.append(log)
            
    db.commit()
    return {"status": "audit_complete", "issues_found": len(flags)}

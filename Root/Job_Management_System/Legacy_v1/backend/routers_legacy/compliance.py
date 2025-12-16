from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..database import get_db
from ..models import JobDescription
from ..services.ncs_service import NCSComplianceService

router = APIRouter(
    prefix="/compliance",
    tags=["NCS Compliance"],
    responses={404: {"description": "Not found"}},
)

service = NCSComplianceService()

class AuditRequest(BaseModel):
    job_id: str
    ncs_code: Optional[str] = None

@router.post("/audit")
def audit_job_compliance(req: AuditRequest, db: Session = Depends(get_db)):
    """
    Audits a Job Description against NCS Standards.
    """
    # Fetch content (In a real app, we'd fetch the JD from DB)
    # Here we assume the frontend sends the ID, and we look it up.
    # If using the 'JobDescription' model:
    job_desc = db.query(JobDescription).filter(JobDescription.job_position_id == req.job_id).first()
    
    if not job_desc:
        # Retry looking up by ID directly if passed ID is generic
        job_desc = db.query(JobDescription).filter(JobDescription.id == req.job_id).first()
    
    if not job_desc:
        # For demo purposes, if no JD exists, create a mock one or error
        # Let's return error to be strict, or fallback to a mock for smooth demo
        raise HTTPException(status_code=404, detail="Job Description not found")
        
    result = service.audit_job_description(job_desc, req.ncs_code)
    return result

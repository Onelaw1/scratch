from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import date
from .. import models, schemas
from datetime import date
from .. import models, schemas
from ..database import get_db
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/personnel",
    tags=["personnel"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER'))]
)

@router.get("/{user_id}/tenure-analysis", response_model=schemas.TenureAnalysis)
def get_tenure_analysis(user_id: str, db: Session = Depends(get_db)):
    """
    Calculates Job Tenure (Expertise) vs Organization Tenure (Loyalty).
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 1. Org Tenure (Loyalty)
    # Simple calculation: Today - Hire Date
    org_tenure_months = 0.0
    if user.hire_date:
        delta = date.today() - user.hire_date
        org_tenure_months = delta.days / 30.44 # Approx month
        
    # 2. Job Tenure (Expertise)
    # Get current position assignment date
    # Implementation: Check JobPosition.assignment_date if exists, else fallback to latest JobHistory change
    job_tenure_months = 0.0
    current_pos_title = "Unassigned"
    
    # Find active position
    job_pos = db.query(models.JobPosition).filter(models.JobPosition.user_id == user.id).first()
    
    if job_pos:
        current_pos_title = job_pos.title
        
        # Determine Start Date of Current Job
        # Strategy: Look at JobHistory for the LAST "POSITION_CHANGE" or "PROMOTION"
        # If no history, assume assignment_date or hire_date
        
        # Let's check if 'assignment_date' is on the model (I added it in models.py check earlier? Yes line 184)
        start_date = job_pos.assignment_date
        
        if not start_date:
            # Fallback to hire date if explicit assignment date is missing
             start_date = user.hire_date
             
        if start_date:
            delta_job = date.today() - start_date
            job_tenure_months = delta_job.days / 30.44

    # 3. Ratio
    ratio = 0.0
    if org_tenure_months > 0:
        ratio = job_tenure_months / org_tenure_months
        
    # 4. Histories
    job_hists = [] 
    if job_pos:
        job_hists = db.query(models.JobHistory).filter(models.JobHistory.job_position_id == job_pos.id).all()
        
    org_hists = db.query(models.OrgHistory).filter(models.OrgHistory.user_id == user.id).all()

    return {
        "user_id": user.id,
        "user_name": user.name,
        "current_job_position": current_pos_title,
        "current_org_unit": user.org_unit.name if user.org_unit else None,
        "job_tenure_months": round(job_tenure_months, 1),
        "org_tenure_months": round(org_tenure_months, 1),
        "expertise_ratio": round(ratio, 2),
        "job_history": job_hists,
        "org_history": org_hists
    }

@router.get("/{user_id}/timeline", response_model=List[Dict[str, Any]])
def get_combined_timeline(user_id: str, db: Session = Depends(get_db)):
    """
    Returns a flattened list of events (Job Changes, Org Changes, Promotions)
    sorted by date for the Visualization UI.
    """
    timeline = []
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")

    # 1. Hire Event
    if user.hire_date:
        timeline.append({
            "date": user.hire_date,
            "type": "HIRE",
            "title": "Joined Company",
            "description": f"Joined as {user.name}"
        })
        
    # 2. Org Changes
    org_hists = db.query(models.OrgHistory).filter(models.OrgHistory.user_id == user_id).all()
    for oh in org_hists:
        timeline.append({
            "date": oh.start_date,
            "type": "ORG_CHANGE",
            "title": "Department Change",
            "description": f"Moved to {oh.org_unit.name if oh.org_unit else 'Unknown'}"
        })
        
    # 3. Job Changes (via JobHistory of current and past positions)
    # Ideally we should link JobHistory to User directly or traverse all positions user held.
    # For MVP, we check current position's history context
    job_pos = db.query(models.JobPosition).filter(models.JobPosition.user_id == user.id).first()
    if job_pos:
        # Assignment
        if job_pos.assignment_date:
             timeline.append({
                "date": job_pos.assignment_date,
                "type": "JOB_ASSIGN",
                "title": "Position Assigned",
                "description": f"Assigned to {job_pos.title}"
            })
            
        j_hists = db.query(models.JobHistory).filter(models.JobHistory.job_position_id == job_pos.id).all()
        for jh in j_hists:
             timeline.append({
                "date": jh.change_date,
                "type": "JOB_UPDATE",
                "title": jh.change_type,
                "description": jh.description
            })
            
    # Sort by Date Descending
    timeline.sort(key=lambda x: x['date'], reverse=True)
    
    return timeline

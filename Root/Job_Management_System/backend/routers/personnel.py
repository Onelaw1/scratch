from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from .. import models
from ..database import get_db

router = APIRouter(
    prefix="/personnel",
    tags=["personnel"],
    responses={404: {"description": "Not found"}},
)

def calculate_months_diff(start_date: date, end_date: date) -> int:
    if not start_date or not end_date:
        return 0
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

@router.get("/{user_id}/tenure")
def get_personnel_tenure(user_id: str, db: Session = Depends(get_db)):
    """
    Returns Dual Tenure information:
    1. Organization Tenure (from hire_date)
    2. Job Tenure (from current position assignment_date)
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    today = date.today()
    
    # 1. Org Tenure
    org_tenure_months = calculate_months_diff(user.hire_date, today)
    
    # 2. Job Tenure
    # Find active position (live model)
    current_pos = None
    for pos in user.job_positions:
        if not pos.is_future_model:
            current_pos = pos
            break
            
    job_tenure_months = 0
    assignment_date = None
    is_expert_candidate = False
    
    if current_pos:
        assignment_date = current_pos.assignment_date
        # If assignment_date is null, we might fallback to hire_date or 0, but 0 is safer for "unknown"
        if assignment_date:
            job_tenure_months = calculate_months_diff(assignment_date, today)
            
        # Expert logic: > 36 months (3 years) in same job
        if job_tenure_months >= 36:
            is_expert_candidate = True

    return {
        "user_id": user.id,
        "name": user.name,
        "org_tenure_months": org_tenure_months,
        "job_tenure_months": job_tenure_months,
        "hire_date": user.hire_date,
        "assignment_date": assignment_date,
        "is_expert_candidate": is_expert_candidate,
        "expertise_level": "Expert" if is_expert_candidate else "Growing"
    }

@router.post("/{user_id}/assign-job")
def assign_job_date(user_id: str, date_str: str, db: Session = Depends(get_db)):
    """
    Helper to set assignment date for demo purposes
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Find active position
    current_pos = None
    for pos in user.job_positions:
        if not pos.is_future_model:
            current_pos = pos
            break
            
    if current_pos:
        from datetime import datetime
        # Parse YYYY-MM-DD
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        current_pos.assignment_date = dt
        db.commit()
        return {"message": "Assignment date updated"}
    
    raise HTTPException(status_code=404, detail="No active position found for user")

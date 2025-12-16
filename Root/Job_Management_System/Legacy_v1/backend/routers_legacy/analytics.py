from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any

from .. import models, schemas
from ..database import get_db
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    dependencies=[Depends(require_roles('ADMIN'))]
)

@router.get("/analytics/headcount-fill-rate")
def get_headcount_fill_rate(institution_id: str, year: int, db: Session = Depends(get_db)):
    """
    Returns Plan vs Actual for each Org Unit.
    """
    # 1. Get Headcount Plans
    plans = db.query(models.HeadcountPlan).filter(
        models.HeadcountPlan.institution_id == institution_id,
        models.HeadcountPlan.year == year
    ).all()
    
    result = []
    for plan in plans:
        # 2. Count Actual Users in this Org Unit
        actual_count = db.query(func.count(models.User.id)).filter(
            models.User.org_unit_id == plan.org_unit_id
        ).scalar()
        
        # Get Org Name
        org = db.query(models.OrgUnit).filter(models.OrgUnit.id == plan.org_unit_id).first()
        org_name = org.name if org else "Unknown"
        
        fill_rate = (actual_count / plan.authorized_count * 100) if plan.authorized_count > 0 else 0
        
        result.append({
            "org_unit": org_name,
            "authorized": plan.authorized_count,
            "actual": actual_count,
            "fill_rate": round(fill_rate, 1)
        })
        
    return result

@router.get("/analytics/span-of-control")
def get_span_of_control(institution_id: str, db: Session = Depends(get_db)):
    """
    Returns Average Span of Control by Job Grade or Position.
    """
    # 1. Get all users with reports_to_id
    # We want to count direct reports for each manager
    
    # Subquery: Count reports per manager
    manager_counts = db.query(
        models.User.reports_to_id, 
        func.count(models.User.id).label('span')
    ).filter(
        models.User.reports_to_id != None
    ).group_by(models.User.reports_to_id).all()
    
    data = []
    for mgr_id, span in manager_counts:
        manager = db.query(models.User).filter(models.User.id == mgr_id).first()
        if manager:
            # Get Job Position Grade
            job = db.query(models.JobPosition).filter(models.JobPosition.user_id == manager.id).first()
            grade = job.grade if job else "N/A"
            title = job.title if job else "Unknown"
            
            data.append({
                "manager_name": manager.name,
                "job_title": title,
                "grade": grade,
                "span": span
            })
            
    return data

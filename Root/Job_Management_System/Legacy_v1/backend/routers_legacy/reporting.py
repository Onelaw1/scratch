from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from .. import crud, models, schemas
from ..database import get_db
from .. import crud, models, schemas
from ..database import get_db
import uuid
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/reporting",
    tags=["reporting"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER'))]
)

@router.get("/job-card/{user_id}")
def get_job_management_card(user_id: str, db: Session = Depends(get_db)):
    """
    Aggregates a comprehensive "Job Management Card" for a user.
    Includes:
    1. Profile (User, OrgUnit)
    2. Current Position (Title, Series, Grade)
    3. Job History (Past positions)
    4. Performance (Latest Review Score/Grade)
    5. Evaluation (Job Grade)
    6. Training (Recent courses)
    """
    
    # 1. Fetch User and Profile
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 2. Current Position
    current_pos = None
    for pos in user.job_positions:
        # Simplistic logic: assume the one without end date or most recent is current
        # For MVP, just taking the first one or the one marked as 'is_future_model=False'
        if not pos.is_future_model: 
            current_pos = pos
            break
            
    # If no current pos found, just take first
    if not current_pos and user.job_positions:
        current_pos = user.job_positions[0]
        
    # 3. Job History
    # Derived from modifications to JobPosition or a separate History table if implemented fully.
    # For now, we can show list of positions assigned to user as history
    history_data = []
    for pos in user.job_positions:
        history_data.append({
            "title": pos.title,
            "period": "2024 - Present" if pos == current_pos else "Past", # Placeholder dates
            "series": pos.series.name if pos.series else "N/A"
        })

    # 4. Performance (Latest)
    latest_review = db.query(models.PerformanceReview)\
        .filter(models.PerformanceReview.user_id == user_id)\
        .order_by(models.PerformanceReview.year.desc())\
        .first()
        
    # 5. Job Evaluation (for current position)
    job_grade = "N/A"
    if current_pos and current_pos.evaluation:
        job_grade = current_pos.evaluation.grade
    elif current_pos:
        job_grade = current_pos.grade # Fallback to position grade
        
    # 6. Training
    trainings = []
    for t in user.trainings:
        trainings.append({
            "program": t.program.name if t.program else "Unknown",
            "date": t.completion_date,
            "status": t.status
        })

    return {
        "profile": {
            "name": user.name,
            "email": user.email,
            "department": user.org_unit.name if user.org_unit else "Unassigned",
            "hire_date": user.hire_date
        },
        "position": {
            "title": current_pos.title if current_pos else "No Position",
            "series": current_pos.series.name if current_pos and current_pos.series else "N/A",
            "group": current_pos.series.group.name if current_pos and current_pos.series and current_pos.series.group else "N/A",
            "grade": job_grade
        },
        "performance": {
            "year": latest_review.year if latest_review else "N/A",
            "grade": latest_review.grade if latest_review else "N/A",
            "score": latest_review.total_score if latest_review else 0
        },
        "history": history_data,
        "trainings": trainings
    }

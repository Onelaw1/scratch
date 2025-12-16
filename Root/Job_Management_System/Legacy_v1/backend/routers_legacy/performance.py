from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..database import get_db
from datetime import date
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/api/performance",
    tags=["performance"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER', 'TEAM_LEAD', 'EMPLOYEE'))]
)

@router.post("/reviews", response_model=schemas.PerformanceReview)
def create_review(review: schemas.PerformanceReviewCreate, db: Session = Depends(get_db)):
    # Check if review already exists for user/year
    existing = db.query(models.PerformanceReview).filter(
        models.PerformanceReview.user_id == review.user_id,
        models.PerformanceReview.year == review.year
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Review already exists for this year")
    
    db_review = models.PerformanceReview(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/reviews/{user_id}/{year}", response_model=schemas.PerformanceReview)
def get_review(user_id: str, year: int, db: Session = Depends(get_db)):
    review = db.query(models.PerformanceReview).filter(
        models.PerformanceReview.user_id == user_id,
        models.PerformanceReview.year == year
    ).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/reviews/{review_id}/goals", response_model=schemas.PerformanceGoal)
def add_goal(review_id: str, goal: schemas.PerformanceGoalCreate, db: Session = Depends(get_db)):
    review = db.query(models.PerformanceReview).filter(models.PerformanceReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if review.status == models.ReviewStatus.FINAL:
        raise HTTPException(status_code=400, detail="Cannot add goals to a finalized review")

    goal_data = goal.dict()
    goal_data["review_id"] = review_id # Ensure link
    db_goal = models.PerformanceGoal(**goal_data)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.put("/goals/{goal_id}", response_model=schemas.PerformanceGoal)
def update_goal(goal_id: str, goal_update: schemas.PerformanceGoalUpdate, db: Session = Depends(get_db)):
    db_goal = db.query(models.PerformanceGoal).filter(models.PerformanceGoal.id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Check review status
    if db_goal.review.status == models.ReviewStatus.FINAL:
        raise HTTPException(status_code=400, detail="Cannot update goals in a finalized review")

    for key, value in goal_update.dict(exclude_unset=True).items():
        setattr(db_goal, key, value)
    
    # Auto-calculate final score for goal if supervisor score is present
    if goal_update.supervisor_score is not None:
        db_goal.final_score = goal_update.supervisor_score # Simplified logic: Supervisor score is final
        
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.post("/reviews/{review_id}/calculate", response_model=schemas.PerformanceReview)
def calculate_review(review_id: str, db: Session = Depends(get_db)):
    review = db.query(models.PerformanceReview).filter(models.PerformanceReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # 1. Calculate Job Performance Score (Weighted Average of Goals)
    total_weight = 0.0
    weighted_sum = 0.0
    
    for goal in review.goals:
        total_weight += goal.weight
        weighted_sum += goal.final_score * (goal.weight / 100.0)
        
    # Normalize if total weight is not 100 (Optional, but good practice)
    # For now, we assume user inputs correct weights or we just take the sum
    review.score_job = weighted_sum
    
    # 2. Calculate Total Score
    # Formula: Common(20%) + Leadership(20%) + Job(60%) - Example Weights
    # Let's use a simple average for now or the weights defined in Grand Principles if any.
    # Assuming: Job 60%, Common 20%, Leadership 20%
    review.total_score = (review.score_job * 0.6) + (review.score_common * 0.2) + (review.score_leadership * 0.2)
    
    # 3. Assign Grade
    if review.total_score >= 90:
        review.grade = "S"
    elif review.total_score >= 80:
        review.grade = "A"
    elif review.total_score >= 70:
        review.grade = "B"
    elif review.total_score >= 60:
        review.grade = "C"
    else:
        review.grade = "D"
        
    db.commit()
    db.refresh(review)
    return review

@router.post("/reviews/{review_id}/finalize", response_model=schemas.PerformanceReview)
def finalize_review(review_id: str, db: Session = Depends(get_db)):
    review = db.query(models.PerformanceReview).filter(models.PerformanceReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
        
    review.status = models.ReviewStatus.FINAL
    review.review_date = date.today()
    db.commit()
    db.refresh(review)
    return review

@router.get("/suggestions/{position_id}", response_model=List[schemas.PerformanceGoalCreate])
def get_goal_suggestions(position_id: str, db: Session = Depends(get_db)):
    """
    Suggests performance goals based on:
    1. Job Description KPIs
    2. High-importance Job Tasks
    """
    suggestions = []
    
    # 1. From Job Description KPIs
    jd = db.query(models.JobDescription).filter(models.JobDescription.job_position_id == position_id).first()
    if jd and jd.kpi_indicators:
        # Split by newlines or commas
        kpis = [k.strip() for k in jd.kpi_indicators.replace('\r', '').split('\n') if k.strip()]
        for kpi in kpis:
            suggestions.append(schemas.PerformanceGoalCreate(
                category="JD_KPI",
                goal_text=kpi,
                weight=0.0
            ))
            
    # 2. From Critical Job Tasks (Top 3 by importance/FTE)
    position = db.query(models.JobPosition).filter(models.JobPosition.id == position_id).first()
    if position:
        # Sort tasks by some metric or just take first few
        for task in position.tasks[:3]:
            suggestions.append(schemas.PerformanceGoalCreate(
                category="JOB_TASK",
                goal_text=f"Execute {task.task_name} effectively",
                weight=0.0
            ))
            
    return suggestions

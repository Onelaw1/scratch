from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/career",
    tags=["career"],
    responses={404: {"description": "Not found"}},
)

# --- Promotion Management ---
@router.get("/promotion-candidates")
def get_promotion_candidates(db: Session = Depends(get_db)):
    """
    Identifies candidates eligible for promotion.
    Logic (MVP):
    - Current Performance Grade is 'S' or 'A'.
    - Position Grade is not the highest (e.g., G5).
    """
    candidates = []
    users = db.query(models.User).all()

    for user in users:
        # Get active position
        current_pos = None
        for pos in user.job_positions:
            if not pos.is_future_model:
                current_pos = pos
                break
        
        if not current_pos:
            continue
            
        # Get latest review
        latest_review = db.query(models.PerformanceReview)\
            .filter(models.PerformanceReview.user_id == user.id)\
            .order_by(models.PerformanceReview.year.desc())\
            .first()
            
        if latest_review and latest_review.grade in ['S', 'A']:
            # Simplistic promotion logic
            candidates.append({
                "user_id": user.id,
                "name": user.name,
                "current_title": current_pos.title,
                "current_grade": current_pos.grade,
                "performance_grade": latest_review.grade,
                "performance_year": latest_review.year,
                "recommended_action": "Promote to Next Grade"
            })
            
    return candidates

# --- Training Recommendations ---
@router.get("/training-recommendations/{user_id}")
def get_training_recommendations(user_id: str, db: Session = Depends(get_db)):
    """
    Suggests training programs based on Job Series.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    recommendations = []
    
    # 1. Get Job Series
    current_series = None
    for pos in user.job_positions:
        if not pos.is_future_model and pos.series:
            current_series = pos.series
            break
            
    if current_series:
        # In a real app, we would query a mapping table Series <-> Training
        # For MVP, returning dummy recommendations based on Series Name
        recommendations.append({
            "id": "trk-1",
            "title": f"Advanced {current_series.name} Workshop",
            "type": "Technical",
            "reason": "Required for current Job Series"
        })
        recommendations.append({
            "id": "trk-2",
            "title": "Leadership Fundamentals",
            "type": "Soft Skills",
            "reason": "General competency gap"
        })

    return recommendations

# --- Competency Modeling ---
@router.get("/competency-model/{series_id}")
def get_competency_model(series_id: str, db: Session = Depends(get_db)):
    """
    Returns the Competency Model (KSA) for a job series.
    """
    series = db.query(models.JobSeries).filter(models.JobSeries.id == series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
        
    # Mock Data for MVP visualization
    # Ideally stored in a Competency or NCS model tables
    return {
        "series_name": series.name,
        "competencies": [
            {"name": "Strategic Planning", "score": 4.5, "type": "Ability"},
            {"name": "Data Analysis", "score": 3.8, "type": "Skill"},
            {"name": "Industry Knowledge", "score": 4.0, "type": "Knowledge"},
            {"name": "Communication", "score": 4.2, "type": "Ability"},
            {"name": "Project Management", "score": 3.5, "type": "Skill"},
        ]
    }

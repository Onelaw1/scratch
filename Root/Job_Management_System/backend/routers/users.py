from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

    users = crud.get_users(db, institution_id=institution_id, skip=skip, limit=limit)
    return users

# --- My Job Dashboard (Employee Experience) ---
@router.get("/me/dashboard")
def read_my_dashboard(db: Session = Depends(get_db)):
    # Mock Auth: Get the first user (e.g., 'EMP001')
    mock_user = db.query(models.User).first()
    if not mock_user:
        raise HTTPException(status_code=404, detail="No users found in database")
        
    # Get Job info
    job_position = db.query(models.JobPosition).filter(models.JobPosition.id == mock_user.job_position_id).first()
    
    # Get Key Tasks (Top 3 by volume?)
    tasks = []
    if job_position:
        tasks = db.query(models.JobTask).filter(models.JobTask.job_position_id == job_position.id).limit(3).all()

    return {
        "user": {
            "name": mock_user.name,
            "title": job_position.title if job_position else "Unassigned",
            "department": "HR Department" # Mock
        },
        "stats": {
            "goals_completed": 12,
            "training_hours": 4.5,
            "pulse_score": "😊"
        },
        "key_tasks": [t.task_name for t in tasks],
        "notifications": [
            {"id": 1, "text": "Annual survey due in 3 days", "type": "warning"},
            {"id": 2, "text": "New Python training available", "type": "info"}
        ]
    }

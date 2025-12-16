from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/strategy",
    tags=["Strategy & Vision"],
    responses={404: {"description": "Not found"}},
)

@router.post("/goals", response_model=schemas.StrategicGoal)
def create_strategic_goal(goal: schemas.StrategicGoalCreate, db: Session = Depends(get_db)):
    """
    <IA Step 1> Create a Strategic Goal.
    All Jobs must eventually link to one of these goals.
    """
    db_goal = models.StrategicGoal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/goals", response_model=List[schemas.StrategicGoal])
def read_strategic_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    goals = db.query(models.StrategicGoal).offset(skip).limit(limit).all()
    return goals

@router.get("/goals/{goal_id}", response_model=schemas.StrategicGoal)
def read_strategic_goal(goal_id: str, db: Session = Depends(get_db)):
    goal = db.query(models.StrategicGoal).filter(models.StrategicGoal.id == goal_id).first()
    if goal is None:
        raise HTTPException(status_code=404, detail="Strategic Goal not found")
    return goal

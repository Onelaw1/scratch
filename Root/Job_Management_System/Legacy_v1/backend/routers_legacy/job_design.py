from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/job-design",
    tags=["Job Design & Analysis"],
    responses={404: {"description": "Not found"}},
)

# --- Job Position ---
@router.post("/positions", response_model=schemas.JobPosition)
def create_job_position(job: schemas.JobPositionCreate, db: Session = Depends(get_db)):
    """
    <IA Step 2> Create a Job Position linked to a Strategic Goal.
    """
    # Verify Strategy
    if job.strategic_goal_id:
        strategy = db.query(models.StrategicGoal).filter(models.StrategicGoal.id == job.strategic_goal_id).first()
        if not strategy:
            raise HTTPException(status_code=400, detail="linked Strategic Goal not found")
            
    db_job = models.JobPosition(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/positions/{job_id}", response_model=schemas.JobPosition)
def read_job_position(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.JobPosition).filter(models.JobPosition.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job Position not found")
    return job

# --- Job Tasks ---
@router.post("/positions/{job_id}/tasks", response_model=schemas.JobTask)
def add_job_task(job_id: str, task: schemas.JobTaskCreate, db: Session = Depends(get_db)):
    db_task = models.JobTask(**task.dict(), job_id=job_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# --- Job Requirements ---
@router.post("/positions/{job_id}/requirements", response_model=schemas.JobRequirement)
def add_job_requirement(job_id: str, req: schemas.JobRequirementCreate, db: Session = Depends(get_db)):
    db_req = models.JobRequirement(**req.dict(), job_id=job_id)
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

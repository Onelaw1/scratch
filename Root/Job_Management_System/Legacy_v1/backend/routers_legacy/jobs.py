from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
import uuid
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN'))]
)

# --- Job Groups ---
@router.post("/groups/", response_model=schemas.JobGroup)
def create_job_group(group: schemas.JobGroupCreate, db: Session = Depends(get_db)):
    db_group = models.JobGroup(
        id=group.id or str(uuid.uuid4()),
        name=group.name
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/groups/", response_model=List[schemas.JobGroup])
def read_job_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JobGroup).offset(skip).limit(limit).all()

# --- Job Series ---
@router.post("/series/", response_model=schemas.JobSeries)
def create_job_series(series: schemas.JobSeriesCreate, db: Session = Depends(get_db)):
    db_series = models.JobSeries(
        id=series.id or str(uuid.uuid4()),
        group_id=series.group_id,
        name=series.name
    )
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series

@router.get("/series/", response_model=List[schemas.JobSeries])
def read_job_series(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JobSeries).offset(skip).limit(limit).all()

# --- Job Positions ---
@router.post("/positions/", response_model=schemas.JobPosition)
def create_job_position(position: schemas.JobPositionCreate, db: Session = Depends(get_db)):
    db_position = models.JobPosition(
        id=position.id or str(uuid.uuid4()),
        series_id=position.series_id,
        title=position.title,
        grade=position.grade
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@router.get("/positions/", response_model=List[schemas.JobPosition])
def read_job_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JobPosition).offset(skip).limit(limit).all()

# --- Legacy Job Endpoints (Keep for compatibility if needed) ---
# --- Legacy Job Endpoints (Keep for compatibility if needed) ---
# @router.post("/{institution_id}", response_model=schemas.Job)
# def create_job(institution_id: str, job: schemas.JobCreate, db: Session = Depends(get_db)):
#     # Simple implementation for legacy support
#     db_job = models.Job(
#         id=str(uuid.uuid4()),
#         institution_id=institution_id,
#         title=job.title,
#         description=job.description
#     )
#     db.add(db_job)
#     db.commit()
#     db.refresh(db_job)
#     return db_job

# @router.get("/{institution_id}", response_model=List[schemas.Job])
# def read_jobs(institution_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return db.query(models.Job).filter(models.Job.institution_id == institution_id).offset(skip).limit(limit).all()

# @router.post("/{job_id}/tasks", response_model=schemas.JobTask)
# def create_task(job_id: str, task: schemas.JobTaskCreate, db: Session = Depends(get_db)):
#     return crud.create_job_task(db=db, task=task, job_id=job_id)

# @router.get("/{job_id}/tasks", response_model=List[schemas.JobTask])
# def read_tasks(job_id: str, db: Session = Depends(get_db)):
#     return crud.get_job_tasks(db, job_id=job_id)

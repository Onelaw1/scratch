from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/job-analysis",
    tags=["job-analysis"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Org Units ---
@router.post("/org-units/", response_model=schemas.OrgUnit)
def create_org_unit(org_unit: schemas.OrgUnitCreate, db: Session = Depends(get_db)):
    db_org_unit = models.OrgUnit(**org_unit.dict())
    db.add(db_org_unit)
    db.commit()
    db.refresh(db_org_unit)
    return db_org_unit

@router.get("/org-units/", response_model=List[schemas.OrgUnit])
def read_org_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.OrgUnit).offset(skip).limit(limit).all()

# --- Job Positions ---
@router.post("/job-positions/", response_model=schemas.JobPosition)
def create_job_position(position: schemas.JobPositionCreate, db: Session = Depends(get_db)):
    db_position = models.JobPosition(**position.dict())
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@router.get("/job-positions/", response_model=List[schemas.JobPosition])
def read_job_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JobPosition).offset(skip).limit(limit).all()

# --- Job Tasks (Auto-Complete Source) ---
@router.post("/job-tasks/", response_model=schemas.JobTask)
def create_job_task(task: schemas.JobTaskCreate, db: Session = Depends(get_db)):
    db_task = models.JobTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/job-tasks/", response_model=List[schemas.JobTask])
def read_job_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JobTask).offset(skip).limit(limit).all()

# --- Workload Entries (Survey Data) ---
@router.post("/workload-entries/", response_model=schemas.WorkloadEntry)
def create_workload_entry(entry: schemas.WorkloadEntryCreate, db: Session = Depends(get_db)):
    # Calculate FTE: (Volume * StandardTime) / 1920 (Annual working hours)
    fte = (entry.volume * entry.standard_time) / 1920.0
    
    # Exclude 'survey_period_id' as it's not in the current model but present in schema for legacy compat
    entry_data = entry.dict(exclude={'survey_period_id'})
    
    db_entry = models.WorkloadEntry(**entry_data, fte=fte)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/workload-entries/", response_model=List[schemas.WorkloadEntry])
def read_workload_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.WorkloadEntry).offset(skip).limit(limit).all()

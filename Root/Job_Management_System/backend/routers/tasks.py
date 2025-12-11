from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

# --- Job Task Endpoints ---

@router.post("/job-tasks", response_model=schemas.JobTask)
def create_job_task(task: schemas.JobTaskCreate, db: Session = Depends(get_db)):
    db_task = models.JobTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/job-tasks/{position_id}", response_model=List[schemas.JobTask])
def read_job_tasks(position_id: str, db: Session = Depends(get_db)):
    return db.query(models.JobTask).filter(models.JobTask.job_position_id == position_id).all()

@router.get("/job-tasks/detail/{task_id}", response_model=schemas.JobTask)
def read_job_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(models.JobTask).filter(models.JobTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Job Task not found")
    return task

@router.put("/job-tasks/{task_id}", response_model=schemas.JobTask)
def update_job_task(task_id: str, task_update: schemas.JobTaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.JobTask).filter(models.JobTask.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Job Task not found")
    
    # Update fields dynamically
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/job-tasks/{task_id}")
def delete_job_task(task_id: str, db: Session = Depends(get_db)):
    db_task = db.query(models.JobTask).filter(models.JobTask.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Job Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Job Task deleted"}

# --- Work Item Endpoints ---

@router.post("/work-items", response_model=schemas.WorkItem)
def create_work_item(work: schemas.WorkItemCreate, db: Session = Depends(get_db)):
    db_work = models.WorkItem(**work.dict())
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work

@router.get("/work-items/{task_id}", response_model=List[schemas.WorkItem])
def read_work_items(task_id: str, db: Session = Depends(get_db)):
    return db.query(models.WorkItem).filter(models.WorkItem.job_task_id == task_id).all()

@router.get("/work-items/detail/{work_id}", response_model=schemas.WorkItem)
def read_work_item(work_id: str, db: Session = Depends(get_db)):
    work = db.query(models.WorkItem).filter(models.WorkItem.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work Item not found")
    return work

@router.put("/work-items/{work_id}", response_model=schemas.WorkItem)
def update_work_item(work_id: str, work_update: schemas.WorkItemUpdate, db: Session = Depends(get_db)):
    db_work = db.query(models.WorkItem).filter(models.WorkItem.id == work_id).first()
    if not db_work:
        raise HTTPException(status_code=404, detail="Work Item not found")
    
    for key, value in work_update.dict(exclude_unset=True).items():
        setattr(db_work, key, value)
        
    db.commit()
    db.refresh(db_work)
    return db_work

@router.delete("/work-items/{work_id}")
def delete_work_item(work_id: str, db: Session = Depends(get_db)):
    db_work = db.query(models.WorkItem).filter(models.WorkItem.id == work_id).first()
    if not db_work:
        raise HTTPException(status_code=404, detail="Work Item not found")
    
    db.delete(db_work)
    db.commit()
    return {"message": "Work Item deleted"}

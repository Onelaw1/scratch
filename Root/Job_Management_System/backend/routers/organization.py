from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/organization",
    tags=["organization"],
    responses={404: {"description": "Not found"}},
)

# --- Job Group ---

@router.post("/groups", response_model=schemas.JobGroup)
def create_job_group(group: schemas.JobGroupCreate, db: Session = Depends(get_db)):
    db_group = models.JobGroup(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/groups/{institution_id}", response_model=List[schemas.JobGroup])
def read_job_groups(institution_id: str, db: Session = Depends(get_db)):
    return db.query(models.JobGroup).filter(models.JobGroup.institution_id == institution_id).all()

@router.get("/groups/detail/{group_id}", response_model=schemas.JobGroup)
def read_job_group(group_id: str, db: Session = Depends(get_db)):
    group = db.query(models.JobGroup).filter(models.JobGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Job Group not found")
    return group

@router.put("/groups/{group_id}", response_model=schemas.JobGroup)
def update_job_group(group_id: str, group_update: schemas.JobGroupUpdate, db: Session = Depends(get_db)):
    db_group = db.query(models.JobGroup).filter(models.JobGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Job Group not found")
    
    if group_update.name:
        db_group.name = group_update.name
        
    db.commit()
    db.refresh(db_group)
    return db_group

@router.delete("/groups/{group_id}")
def delete_job_group(group_id: str, db: Session = Depends(get_db)):
    db_group = db.query(models.JobGroup).filter(models.JobGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Job Group not found")
    
    db.delete(db_group)
    db.commit()
    return {"message": "Job Group deleted"}

# --- Job Series ---

@router.post("/series", response_model=schemas.JobSeries)
def create_job_series(series: schemas.JobSeriesCreate, db: Session = Depends(get_db)):
    db_series = models.JobSeries(**series.dict())
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series

@router.get("/series/{group_id}", response_model=List[schemas.JobSeries])
def read_job_series_list(group_id: str, db: Session = Depends(get_db)):
    return db.query(models.JobSeries).filter(models.JobSeries.group_id == group_id).all()

@router.get("/series/detail/{series_id}", response_model=schemas.JobSeries)
def read_job_series(series_id: str, db: Session = Depends(get_db)):
    series = db.query(models.JobSeries).filter(models.JobSeries.id == series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="Job Series not found")
    return series

@router.put("/series/{series_id}", response_model=schemas.JobSeries)
def update_job_series(series_id: str, series_update: schemas.JobSeriesUpdate, db: Session = Depends(get_db)):
    db_series = db.query(models.JobSeries).filter(models.JobSeries.id == series_id).first()
    if not db_series:
        raise HTTPException(status_code=404, detail="Job Series not found")
    
    if series_update.name:
        db_series.name = series_update.name
    if series_update.ncs_code:
        db_series.ncs_code = series_update.ncs_code
    if series_update.ncs_name:
        db_series.ncs_name = series_update.ncs_name
        
    db.commit()
    db.refresh(db_series)
    return db_series

@router.delete("/series/{series_id}")
def delete_job_series(series_id: str, db: Session = Depends(get_db)):
    db_series = db.query(models.JobSeries).filter(models.JobSeries.id == series_id).first()
    if not db_series:
        raise HTTPException(status_code=404, detail="Job Series not found")
    
    db.delete(db_series)
    db.commit()
    return {"message": "Job Series deleted"}

# --- Job Position ---

@router.post("/positions", response_model=schemas.JobPosition)
def create_job_position(position: schemas.JobPositionCreate, db: Session = Depends(get_db)):
    db_position = models.JobPosition(**position.dict())
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@router.get("/positions/{series_id}", response_model=List[schemas.JobPosition])
def read_job_positions(series_id: str, db: Session = Depends(get_db)):
    return db.query(models.JobPosition).filter(models.JobPosition.series_id == series_id).all()

@router.get("/positions/detail/{position_id}", response_model=schemas.JobPosition)
def read_job_position(position_id: str, db: Session = Depends(get_db)):
    position = db.query(models.JobPosition).filter(models.JobPosition.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Job Position not found")
    return position

@router.put("/positions/{position_id}", response_model=schemas.JobPosition)
def update_job_position(position_id: str, position_update: schemas.JobPositionUpdate, db: Session = Depends(get_db)):
    db_position = db.query(models.JobPosition).filter(models.JobPosition.id == position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="Job Position not found")
    
    if position_update.title:
        db_position.title = position_update.title
    if position_update.grade:
        db_position.grade = position_update.grade
    if position_update.is_future_model is not None:
        db_position.is_future_model = position_update.is_future_model
        
    db.commit()
    db.refresh(db_position)
    return db_position

@router.delete("/positions/{position_id}")
def delete_job_position(position_id: str, db: Session = Depends(get_db)):
    db_position = db.query(models.JobPosition).filter(models.JobPosition.id == position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="Job Position not found")
    
    db.delete(db_position)
    db.commit()
    return {"message": "Job Position deleted"}

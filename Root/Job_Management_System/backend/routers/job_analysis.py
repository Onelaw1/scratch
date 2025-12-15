from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
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

# --- Analysis & Aggregation ---
@router.get("/analysis/fte-by-org")
def get_fte_by_org(db: Session = Depends(get_db)):
    results = db.query(
        models.OrgUnit.name,
        func.sum(models.WorkloadEntry.fte).label("total_fte")
    ).join(models.User, models.WorkloadEntry.user_id == models.User.id)\
     .join(models.OrgUnit, models.User.org_unit_id == models.OrgUnit.id)\
     .group_by(models.OrgUnit.id, models.OrgUnit.name).all()
    
    return [{"name": r[0], "fte": r[1]} for r in results]

@router.get("/analysis/fte-by-position")
def get_fte_by_position(db: Session = Depends(get_db)):
    results = db.query(
        models.JobPosition.title,
        func.sum(models.WorkloadEntry.fte).label("total_fte")
    ).join(models.JobTask, models.WorkloadEntry.task_id == models.JobTask.id)\
     .join(models.JobPosition, models.JobTask.job_position_id == models.JobPosition.id)\
     .group_by(models.JobPosition.id, models.JobPosition.title).all()
     
    return [{"name": r[0], "fte": r[1]} for r in results]

# --- Productivity (HCROI / HCVA) ---
@router.post("/productivity/financial", response_model=schemas.FinancialPerformance)
def create_financial_performance(data: schemas.FinancialPerformanceCreate, db: Session = Depends(get_db)):
    # Calculate Net Income
    net_income = data.revenue - (data.operating_expenses + data.personnel_costs)
    
    db_obj = models.FinancialPerformance(**data.dict(), net_income=net_income)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/productivity/metrics/{institution_id}")
def get_productivity_metrics(institution_id: str, db: Session = Depends(get_db)):
    # 1. Get Financial Data (Latest Year)
    fin_data = db.query(models.FinancialPerformance)\
        .filter(models.FinancialPerformance.institution_id == institution_id)\
        .order_by(models.FinancialPerformance.year.desc())\
        .first()
        
    if not fin_data:
        raise HTTPException(status_code=404, detail="No financial data found")
        
    # 2. Calculate Total FTE for that Institution
    # (Simplified: Sum of all current workload entries. Ideally should be snapshot by year)
    total_fte_res = db.query(func.sum(models.WorkloadEntry.fte))\
        .join(models.User, models.WorkloadEntry.user_id == models.User.id)\
        .filter(models.User.institution_id == institution_id)\
        .scalar()
        
    total_fte = total_fte_res if total_fte_res else 0.0
    
    if total_fte == 0 or fin_data.personnel_costs == 0:
        return {
            "year": fin_data.year,
            "hcroi": 0.0,
            "hcva": 0.0,
            "revenue_per_fte": 0.0,
            "message": "Insufficient data for calculation"
        }

    # 3. Calculate Metrics
    # HCROI = (Revenue - (OpEx - PersonnelCost?? No, OpEx typically excludes personnel)) 
    # Formula: (Revenue - (Total Expenses - Personnel Cost)) / Personnel Cost
    # Here OpEx excludes personnel, so Total Expenses = OpEx + Personnel
    # Adjusted Revenue = Revenue - OpEx
    adjusted_revenue = fin_data.revenue - fin_data.operating_expenses
    hcroi = adjusted_revenue / fin_data.personnel_costs
    
    # HCVA = Adjusted Revenue / FTE
    hcva = adjusted_revenue / total_fte
    
    return {
        "year": fin_data.year,
        "hcroi": round(hcroi, 2),
        "hcva": round(hcva, 2), # Value Added per FTE
        "revenue_per_fte": round(fin_data.revenue / total_fte, 2),
        "total_fte": round(total_fte, 1)
    }

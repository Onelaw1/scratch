from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from .. import models, schemas
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/workforce",
    tags=["workforce"],
    responses={404: {"description": "Not found"}},
)

# --- FTE Calculation ---

@router.post("/calculate-fte", response_model=schemas.WorkloadEntry)
def calculate_fte(entry: schemas.WorkloadEntryCreate, db: Session = Depends(get_db)):
    """
    Calculate FTE based on standard time and volume.
    FTE = (Standard Time * Volume) / 1920 (Annual Standard Hours)
    """
    # Create entry using existing CRUD logic which handles FTE calculation
    db_entry = models.WorkloadEntry(**entry.dict())
    
    if db_entry.standard_time and db_entry.volume:
        db_entry.fte = (db_entry.standard_time * db_entry.volume) / 1920.0
    else:
        db_entry.fte = 0.0

    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# --- Productivity Analysis ---

@router.get("/productivity-analysis/{institution_id}", response_model=Dict[str, Any])
def get_productivity_analysis(institution_id: str, db: Session = Depends(get_db)):
    """
    Compare current vs. required headcount (FTE) for an institution.
    """
    # 1. Get all users in the institution
    users = db.query(models.User).filter(models.User.institution_id == institution_id).all()
    current_headcount = len(users)
    
    # 2. Calculate total required FTE from workload entries
    # This assumes we are looking at the latest active survey period or all entries
    # For simplicity, we'll sum all FTEs for now. In production, filter by survey period.
    total_fte = 0.0
    workload_entries = db.query(models.WorkloadEntry).join(models.User).filter(models.User.institution_id == institution_id).all()
    
    for entry in workload_entries:
        total_fte += entry.fte
        
    # 3. Calculate productivity ratio
    productivity_ratio = (total_fte / current_headcount * 100) if current_headcount > 0 else 0.0
    
    return {
        "institution_id": institution_id,
        "current_headcount": current_headcount,
        "required_fte": round(total_fte, 2),
        "productivity_ratio": round(productivity_ratio, 2),
        "status": "Overstaffed" if current_headcount > total_fte else "Understaffed"
    }

# --- Future Trend Analysis ---

@router.get("/trend-analysis/{institution_id}", response_model=Dict[str, Any])
def get_trend_analysis(institution_id: str, years: int = 5, db: Session = Depends(get_db)):
    """
    Project future headcount requirements based on simple linear growth assumption (e.g., 2% per year).
    """
    # Get current required FTE
    total_fte = 0.0
    workload_entries = db.query(models.WorkloadEntry).join(models.User).filter(models.User.institution_id == institution_id).all()
    for entry in workload_entries:
        total_fte += entry.fte
        
    growth_rate = 0.02 # 2% growth assumption
    projections = []
    
    current_year = datetime.now().year
    
    for i in range(years):
        year = current_year + i
        projected_fte = total_fte * ((1 + growth_rate) ** i)
        projections.append({
            "year": year,
            "projected_fte": round(projected_fte, 2)
        })
        
    return {
        "institution_id": institution_id,
        "base_fte": round(total_fte, 2),
        "growth_rate": growth_rate,
        "projections": projections
    }

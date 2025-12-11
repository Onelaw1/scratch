from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/strategy",
    tags=["strategy"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.StrategicAnalysis)
def create_analysis(analysis: schemas.StrategicAnalysisCreate, db: Session = Depends(get_db)):
    # Verify institution exists
    inst = crud.get_institution(db, institution_id=analysis.institution_id)
    if not inst:
        raise HTTPException(status_code=404, detail="Institution not found")
    
    # Validate JSON content
    try:
        json.loads(analysis.content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON content")

    return crud.create_strategic_analysis(db=db, analysis=analysis)

@router.get("/{analysis_id}", response_model=schemas.StrategicAnalysis)
def read_analysis(analysis_id: str, db: Session = Depends(get_db)):
    db_analysis = crud.get_strategic_analysis(db, analysis_id=analysis_id)
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return db_analysis

@router.get("/institution/{institution_id}", response_model=List[schemas.StrategicAnalysis])
def read_analyses_by_institution(institution_id: str, analysis_type: Optional[str] = None, db: Session = Depends(get_db)):
    # Note: crud.get_strategic_analyses currently only filters by institution_id.
    # If analysis_type filtering is needed, we might need to update CRUD or filter here.
    # For now, let's filter in python if needed or update CRUD.
    # The original code filtered by analysis_type. Let's update CRUD to support it or filter here.
    # Since I didn't add analysis_type to CRUD, I will filter here for now, but ideally CRUD should handle it.
    
    analyses = crud.get_strategic_analyses(db, institution_id=institution_id)
    if analysis_type:
        analyses = [a for a in analyses if a.analysis_type == analysis_type]
    return analyses

@router.put("/{analysis_id}", response_model=schemas.StrategicAnalysis)
def update_analysis(analysis_id: str, analysis: schemas.StrategicAnalysisUpdate, db: Session = Depends(get_db)):
    db_analysis = crud.get_strategic_analysis(db, analysis_id=analysis_id)
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis.content:
        try:
            json.loads(analysis.content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON content")
            
    return crud.update_strategic_analysis(db=db, analysis_id=analysis_id, analysis_update=analysis)

@router.delete("/{analysis_id}")
def delete_analysis(analysis_id: str, db: Session = Depends(get_db)):
    db_analysis = crud.get_strategic_analysis(db, analysis_id=analysis_id)
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    crud.delete_strategic_analysis(db, analysis_id=analysis_id)
    return {"ok": True}

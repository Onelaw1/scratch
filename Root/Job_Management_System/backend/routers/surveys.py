from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/surveys",
    tags=["surveys"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{institution_id}", response_model=schemas.SurveyPeriod)
def create_survey(institution_id: str, survey: schemas.SurveyPeriodCreate, db: Session = Depends(get_db)):
    return crud.create_survey_period(db=db, survey=survey, institution_id=institution_id)

@router.get("/{institution_id}", response_model=List[schemas.SurveyPeriod])
def read_surveys(institution_id: str, db: Session = Depends(get_db)):
    return crud.get_survey_periods(db, institution_id=institution_id)

@router.post("/{survey_id}/entries", response_model=schemas.WorkloadEntry)
def create_entry(survey_id: str, entry: schemas.WorkloadEntryCreate, db: Session = Depends(get_db)):
    # Ensure entry.survey_period_id matches survey_id
    if entry.survey_period_id != survey_id:
        raise HTTPException(status_code=400, detail="Survey ID mismatch")
    return crud.create_workload_entry(db=db, entry=entry)

@router.get("/{survey_id}/entries", response_model=List[schemas.WorkloadEntry])
def read_entries(survey_id: str, db: Session = Depends(get_db)):
    return crud.get_workload_entries(db, survey_period_id=survey_id)

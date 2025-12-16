from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from .. import crud, models, schemas
from ..database import get_db
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/surveys",
    tags=["surveys"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN'))]
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

# --- Employee Experience (Pulse) ---
class PulseCreate(BaseModel):
    mood: int # 1-5
    workload: str # LOW, NORMAL, HIGH, OVERLOAD
    note: Optional[str] = None

@router.post("/pulse")
def create_pulse_check(pulse: PulseCreate, db: Session = Depends(get_db)):
    # Mock User
    mock_user = db.query(models.User).first()
    if not mock_user:
        raise HTTPException(status_code=400, detail="No user found")
        
    db_pulse = models.DailyPulse(
        user_id=mock_user.id,
        mood_score=pulse.mood,
        workload_level=models.PulseWorkloadLevel(pulse.workload),
        note=pulse.note
    )
    db.add(db_pulse)
    db.commit()
    db.refresh(db_pulse)
    return {"status": "success", "id": db_pulse.id}

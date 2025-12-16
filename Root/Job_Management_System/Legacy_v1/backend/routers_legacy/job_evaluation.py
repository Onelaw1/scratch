from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/job-evaluation",
    tags=["Job Evaluation & Compensation"],
    responses={404: {"description": "Not found"}},
)

# --- Criteria ---
@router.post("/criteria", response_model=schemas.JobEvaluationCriteria)
def create_criteria(criteria: schemas.JobEvaluationCriteriaBase, db: Session = Depends(get_db)):
    db_criteria = models.JobEvaluationCriteria(**criteria.dict())
    db.add(db_criteria)
    db.commit()
    db.refresh(db_criteria)
    return db_criteria

@router.get("/criteria", response_model=List[schemas.JobEvaluationCriteria])
def read_criteria(db: Session = Depends(get_db)):
    return db.query(models.JobEvaluationCriteria).all()

# --- Evaluation Execution ---
@router.post("/positions/{job_id}/evaluate", response_model=schemas.JobEvaluationResult)
def evaluate_job(job_id: str, evaluation: schemas.JobEvaluationResultCreate, db: Session = Depends(get_db)):
    """
    <IA Step 3> Perform Job Evaluation (Logic DB).
    Calculates total score and assigns Grade based on logic.
    """
    # 1. Calculate Total Score
    total_score = sum([s.score for s in evaluation.scores])
    
    # 2. Logic: Assign Grade based on Score (Simple Logic for now)
    grade = None
    if total_score >= 90: grade = models.JobGrade.EXECUTIVE
    elif total_score >= 80: grade = models.JobGrade.G5
    elif total_score >= 60: grade = models.JobGrade.G4
    elif total_score >= 40: grade = models.JobGrade.G3
    elif total_score >= 20: grade = models.JobGrade.G2
    else: grade = models.JobGrade.G1
    
    # 3. Save Result
    db_result = models.JobEvaluationResult(
        job_id=job_id,
        total_score=total_score,
        grade=grade,
        status="CONFIRMED"
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    
    # 4. Save Scores
    for score_item in evaluation.scores:
        db_score = models.JobEvaluationScore(
            result_id=db_result.id,
            criteria_id=score_item.criteria_id,
            score=score_item.score,
            notes=score_item.notes
        )
        db.add(db_score)
    db.commit()
    
    return db_result

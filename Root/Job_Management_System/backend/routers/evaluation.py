from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
import uuid
import statistics

router = APIRouter(
    prefix="/evaluations",
    tags=["evaluations"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.JobEvaluation)
def create_evaluation(evaluation: schemas.JobEvaluationCreate, db: Session = Depends(get_db)):
    # Check if evaluation already exists for this position
    existing = db.query(models.JobEvaluation).filter(
        models.JobEvaluation.job_position_id == evaluation.job_position_id
    ).first()
    
    if existing:
        return existing

    db_eval = models.JobEvaluation(
        id=str(uuid.uuid4()),
        job_position_id=evaluation.job_position_id,
        total_score=0.0
    )
    db.add(db_eval)
    db.commit()
    db.refresh(db_eval)
    return db_eval

@router.post("/{evaluation_id}/scores", response_model=schemas.JobEvaluationScore)
def add_score(
    evaluation_id: str, 
    score: schemas.JobEvaluationScoreCreate, 
    db: Session = Depends(get_db)
):
    # Calculate raw total
    raw_total = score.score_expertise + score.score_responsibility + score.score_complexity
    
    db_score = models.JobEvaluationScore(
        id=str(uuid.uuid4()),
        evaluation_id=evaluation_id,
        rater_type=score.rater_type,
        rater_user_id=score.rater_user_id,
        score_expertise=score.score_expertise,
        score_responsibility=score.score_responsibility,
        score_complexity=score.score_complexity,
        raw_total=raw_total,
        z_score=0.0, # Will be calculated later
        final_score=0.0 # Will be calculated later
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

@router.post("/{evaluation_id}/calculate", response_model=schemas.JobEvaluation)
def calculate_results(evaluation_id: str, db: Session = Depends(get_db)):
    evaluation = db.query(models.JobEvaluation).filter(models.JobEvaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    scores = db.query(models.JobEvaluationScore).filter(models.JobEvaluationScore.evaluation_id == evaluation_id).all()
    
    if not scores:
        return evaluation

    # 1. Calculate Mean and Stdev for Z-Score (Simulated Population)
    # In a real system, this would be based on ALL evaluations in the organization.
    # Here, we simulate a population mean of 150 and stdev of 30 for demonstration.
    POPULATION_MEAN = 150.0
    POPULATION_STDEV = 30.0
    
    # 2. Apply Weights
    weights = {
        models.RaterType.SELF: 0.1,
        models.RaterType.PEER: 0.2,
        models.RaterType.SUPERVISOR_1: 0.3,
        models.RaterType.SUPERVISOR_2: 0.2,
        models.RaterType.EXTERNAL: 0.2
    }
    
    final_total_score = 0.0
    total_weight = 0.0
    
    for s in scores:
        # Calculate Z-Score
        s.z_score = (s.raw_total - POPULATION_MEAN) / POPULATION_STDEV
        
        # Calculate Weighted Score (Simple weighted average of raw scores for now, 
        # but could use Z-score for adjustment)
        weight = weights.get(s.rater_type, 0.0)
        s.final_score = s.raw_total * weight
        
        final_total_score += s.raw_total * weight # This is a simplified aggregation
        total_weight += weight
        
    # Normalize if weights don't sum to 1 (e.g. missing raters)
    if total_weight > 0:
        final_total_score = final_total_score / total_weight
    
    evaluation.total_score = final_total_score
    
    # 3. Assign Grade
    if final_total_score >= 240:
        evaluation.grade = models.JobGrade.G1
    elif final_total_score >= 180:
        evaluation.grade = models.JobGrade.G2
    elif final_total_score >= 120:
        evaluation.grade = models.JobGrade.G3
    elif final_total_score >= 60:
        evaluation.grade = models.JobGrade.G4
    else:
        evaluation.grade = models.JobGrade.G5
        
    db.commit()
    db.refresh(evaluation)
    return evaluation

@router.get("/{evaluation_id}", response_model=schemas.JobEvaluation)
def read_evaluation(evaluation_id: str, db: Session = Depends(get_db)):
    evaluation = db.query(models.JobEvaluation).filter(models.JobEvaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

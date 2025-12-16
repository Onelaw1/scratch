from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4

from .. import models, schemas
from ..database import get_db
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER', 'EVALUATION_COMMITTEE'))]
)

# --- Sessions ---
@router.post("/sessions/", response_model=schemas.EvaluationSession)
def create_session(session: schemas.EvaluationSessionCreate, db: Session = Depends(get_db)):
    db_session = models.EvaluationSession(**session.dict(), id=str(uuid4()))
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/sessions/", response_model=List[schemas.EvaluationSession])
def get_sessions(institution_id: str, db: Session = Depends(get_db)):
    return db.query(models.EvaluationSession).filter(models.EvaluationSession.institution_id == institution_id).all()

# --- Criteria ---
@router.post("/criteria/", response_model=schemas.EvaluationCriteria)
def create_criteria(criteria: schemas.EvaluationCriteriaCreate, db: Session = Depends(get_db)):
    db_criteria = models.EvaluationCriteria(**criteria.dict(), id=str(uuid4()))
    db.add(db_criteria)
    db.commit()
    db.refresh(db_criteria)
    return db_criteria

@router.get("/sessions/{session_id}/criteria", response_model=List[schemas.EvaluationCriteria])
def get_session_criteria(session_id: str, db: Session = Depends(get_db)):
    return db.query(models.EvaluationCriteria).filter(models.EvaluationCriteria.session_id == session_id).all()

# --- Evaluations (Ratings) ---
@router.post("/evaluations/", response_model=schemas.JobEvaluation)
def create_or_get_evaluation(evaluation: schemas.JobEvaluationCreate, db: Session = Depends(get_db)):
    # Check if exists
    db_eval = db.query(models.JobEvaluation).filter(
        models.JobEvaluation.job_position_id == evaluation.job_position_id,
        models.JobEvaluation.session_id == evaluation.session_id
    ).first()
    
    if db_eval:
        return db_eval
        
    db_eval = models.JobEvaluation(**evaluation.dict(), id=str(uuid4()))
    db.add(db_eval)
    db.commit()
    db.refresh(db_eval)
    return db_eval

@router.post("/ratings/", response_model=schemas.JobEvaluationScore)
def submit_rating(rating: schemas.JobEvaluationScoreCreate, db: Session = Depends(get_db)):
    # Calculate raw_total based on factor scores
    score_data = rating.dict()
    # factor_scores is Dict[str, float]
    
    db_rating = models.JobEvaluationScore(**score_data, id=str(uuid4()))
    
    # Simple Logic: Sum of values as raw_total
    if rating.factor_scores:
        db_rating.raw_total = sum(rating.factor_scores.values())
    
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/evaluations/{evaluation_id}", response_model=schemas.JobEvaluation)
def get_evaluation_detail(evaluation_id: str, db: Session = Depends(get_db)):
    return db.query(models.JobEvaluation).filter(models.JobEvaluation.id == evaluation_id).first()

@router.get("/my-assignments", response_model=List[schemas.EvaluationAssignment])
def get_my_assignments(session_id: str, user_id: str, db: Session = Depends(get_db)):
    # In real app, user_id should come from Token
    from ..services.evaluation_logic import EvaluationLogicService
    return EvaluationLogicService.get_my_assignments(db, session_id, user_id)

@router.post("/sessions/{session_id}/matrix_submission", response_model=schemas.MatrixSubmissionResult)
def submit_matrix(session_id: str, submission: schemas.MatrixSubmission, dry_run: bool = False, db: Session = Depends(get_db)):
    from ..services.evaluation_logic import EvaluationLogicService

    # 1. Dry Run / Impact Analysis
    if dry_run:
        analysis = EvaluationLogicService.analyze_rater_bias(
            db, session_id, submission.rater_user_id, submission.ratings
        )
        # We need a schema for this, but for now we can bundle it in result or throw proper return
        # Since response_model is MatrixSubmissionResult, we might need to change it or return JSONResponse
        # For simplicity, let's extend MatrixSubmissionResult or return a dict if dry_run
        return {
            "processed_count": len(submission.ratings),
            "session_id": session_id,
            "analysis": analysis,
            "dry_run": True
        }

    count = 0
    # Process each rating in the matrix
    for rating in submission.ratings:
        # VALIDATION: Check Access
        if submission.rater_user_id:
             allowed = EvaluationLogicService.validate_evaluation_access(
                 db, session_id, submission.rater_user_id, rating.job_position_id
             )
             if not allowed:
                 # Skip or Error? Let's skip and warn, or error.
                 # For Matrix, maybe just ignore unassigned?
                 # print(f"Skipping unauthorized rating: {submission.rater_user_id} -> {rating.job_position_id}")
                 continue

        # 1. Ensure JobEvaluation exists (Concept: Job + Session)
        db_eval = db.query(models.JobEvaluation).filter(
            models.JobEvaluation.job_position_id == rating.job_position_id,
            models.JobEvaluation.session_id == session_id
        ).first()
        
        if not db_eval:
            db_eval = models.JobEvaluation(
                id=str(uuid4()),
                job_position_id=rating.job_position_id,
                session_id=session_id,
                scores=[]
            )
            db.add(db_eval)
            db.flush() # Get ID
            
        # 2. Add or Update Score Record
        raw_total = sum(rating.factor_scores.values()) if rating.factor_scores else 0
        
        # Check if this rater already rated this job in this session
        db_score = db.query(models.JobEvaluationScore).filter(
            models.JobEvaluationScore.evaluation_id == db_eval.id,
            models.JobEvaluationScore.rater_type == submission.rater_type,
            models.JobEvaluationScore.rater_user_id == submission.rater_user_id
        ).first()

        if db_score:
            # Update existing
            db_score.factor_scores = rating.factor_scores
            db_score.raw_total = raw_total
        else:
            # Insert new
            db_score = models.JobEvaluationScore(
                id=str(uuid4()),
                evaluation_id=db_eval.id,
                rater_type=submission.rater_type,
                rater_user_id=submission.rater_user_id,
                factor_scores=rating.factor_scores,
                raw_total=raw_total
            )
            db.add(db_score)
        
        count += 1
        
    db.commit()
    return schemas.MatrixSubmissionResult(processed_count=count, session_id=session_id)

@router.get("/sessions/{session_id}/matrix_submission", response_model=schemas.MatrixSubmission)
def get_matrix_submission(session_id: str, rater_type: str, rater_user_id: str = None, db: Session = Depends(get_db)):
    # 1. Find all JobEvaluations for this session
    evals = db.query(models.JobEvaluation).filter(
        models.JobEvaluation.session_id == session_id
    ).all()
    
    ratings_list = []
    
    for ev in evals:
        # 2. Find score for this rater
        query = db.query(models.JobEvaluationScore).filter(
            models.JobEvaluationScore.evaluation_id == ev.id,
            models.JobEvaluationScore.rater_type == rater_type
        )
        if rater_user_id:
            query = query.filter(models.JobEvaluationScore.rater_user_id == rater_user_id)
        else:
            query = query.filter(models.JobEvaluationScore.rater_user_id == None)
            
        score = query.first()
        
        if score:
            ratings_list.append(schemas.MatrixRatingEntry(
                job_position_id=ev.job_position_id,
                factor_scores=score.factor_scores or {}
            ))
            
    return schemas.MatrixSubmission(
        session_id=session_id,
        rater_type=rater_type,
        rater_user_id=rater_user_id,
        ratings=ratings_list
    )

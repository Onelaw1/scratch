from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
from .. import models, schemas
from ..database import get_db
# RBAC: Admin Only
from ..dependencies import require_roles

router = APIRouter(
    prefix="/admin/evaluations",
    tags=["Start Strategic HR - Admin"],
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER'))]
)

@router.post("/assignments", response_model=List[schemas.EvaluationAssignment])
def create_assignments(assignments: List[schemas.EvaluationAssignmentCreate], db: Session = Depends(get_db)):
    """
    Bulk create evaluation assignments.
    """
    created = []
    for a in assignments:
        # Check existence
        existing = db.query(models.EvaluationAssignment).filter(
            models.EvaluationAssignment.session_id == a.session_id,
            models.EvaluationAssignment.rater_user_id == a.rater_user_id,
            models.EvaluationAssignment.target_job_position_id == a.target_job_position_id
        ).first()
        
        if not existing:
            db_obj = models.EvaluationAssignment(
                **a.dict(),
                id=str(uuid4())
            )
            db.add(db_obj)
            created.append(db_obj)
            
    db.commit()
    return created

@router.get("/assignments", response_model=List[schemas.EvaluationAssignment])
def get_assignments(session_id: str, db: Session = Depends(get_db)):
    """
    Get all assignments for a session (for visualization).
    """
    return db.query(models.EvaluationAssignment).filter(
        models.EvaluationAssignment.session_id == session_id
    ).all()

@router.post("/assignments/auto-assign")
def auto_assign_evaluators(session_id: str, db: Session = Depends(get_db)):
    """
    Auto-generate assignments based on Org Structure:
    1. Employees -> Peers in same OrgUnit (Not Implemented yet, placeholder)
    2. Dept Head -> All Members of OrgUnit
    3. Inst Head -> All Job Positions
    """
    # Placeholder for complex logic
    return {"message": "Auto-assignment logic not fully implemented yet."}

@router.put("/criteria/{criteria_id}", response_model=schemas.EvaluationCriteria)
def update_criteria(criteria_id: str, update_data: schemas.EvaluationCriteriaBase, db: Session = Depends(get_db)):
    c = db.query(models.EvaluationCriteria).filter(models.EvaluationCriteria.id == criteria_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Criteria not found")
        
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(c, key, value)
        
    db.commit()
    db.refresh(c)
    return c

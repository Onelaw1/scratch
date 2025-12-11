from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from datetime import date

router = APIRouter(
    prefix="/api/training",
    tags=["training"],
    responses={404: {"description": "Not found"}},
)

@router.post("/programs", response_model=schemas.TrainingProgram)
def create_program(program: schemas.TrainingProgramCreate, db: Session = Depends(get_db)):
    db_program = models.TrainingProgram(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

@router.get("/programs", response_model=List[schemas.TrainingProgram])
def get_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.TrainingProgram).offset(skip).limit(limit).all()

@router.post("/assign", response_model=schemas.EmployeeTraining)
def assign_training(training: schemas.EmployeeTrainingCreate, db: Session = Depends(get_db)):
    # Check if already assigned
    existing = db.query(models.EmployeeTraining).filter(
        models.EmployeeTraining.user_id == training.user_id,
        models.EmployeeTraining.program_id == training.program_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Training program already assigned to this user")

    db_training = models.EmployeeTraining(**training.dict())
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training

@router.put("/status/{training_id}", response_model=schemas.EmployeeTraining)
def update_training_status(training_id: str, update: schemas.EmployeeTrainingUpdate, db: Session = Depends(get_db)):
    db_training = db.query(models.EmployeeTraining).filter(models.EmployeeTraining.id == training_id).first()
    if not db_training:
        raise HTTPException(status_code=404, detail="Training record not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_training, key, value)
        
    db.commit()
    db.refresh(db_training)
    return db_training

@router.get("/user/{user_id}", response_model=List[schemas.EmployeeTraining])
def get_user_training(user_id: str, db: Session = Depends(get_db)):
    return db.query(models.EmployeeTraining).filter(models.EmployeeTraining.user_id == user_id).all()

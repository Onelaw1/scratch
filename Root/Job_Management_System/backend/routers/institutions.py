from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/institutions",
    tags=["institutions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Institution)
def create_institution(institution: schemas.InstitutionCreate, db: Session = Depends(get_db)):
    return crud.create_institution(db=db, institution=institution)

@router.get("/", response_model=List[schemas.Institution])
def read_institutions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    institutions = crud.get_institutions(db, skip=skip, limit=limit)
    return institutions

@router.get("/{institution_id}", response_model=schemas.Institution)
def read_institution(institution_id: str, db: Session = Depends(get_db)):
    db_institution = crud.get_institution(db, institution_id=institution_id)
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")
    return db_institution

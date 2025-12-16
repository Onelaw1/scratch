from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database import get_db
from ..services.integral_service import IntegralService

router = APIRouter(
    prefix="/scientific/performance",
    tags=["Scientific HR"],
    responses={404: {"description": "Not found"}},
)

service = IntegralService()

@router.get("/integral/all")
def get_all_performance_integrals(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Returns integral analysis for all users (Leaderboard).
    """
    return service.get_all_integrals(db)

@router.get("/integral/{user_id}")
def get_performance_integral(user_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Returns longitudinal performance integral for a specific user.
    """
    return service.calculate_integral(db, user_id)

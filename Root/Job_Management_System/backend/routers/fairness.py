from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.fairness_service import FairnessService

router = APIRouter(
    prefix="/fairness",
    tags=["Fairness & DEI"],
    responses={404: {"description": "Not found"}},
)

service = FairnessService()

@router.get("/analysis")
def get_fairness_analysis(db: Session = Depends(get_db)):
    """
    Returns data for DEI Dashboard: Pay Gaps, Age Correlation, Outliers.
    """
    return service.analyze_fairness(db)

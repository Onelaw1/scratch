from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.workforce_service import WorkforceService

router = APIRouter(
    prefix="/scientific/workforce",
    tags=["Scientific Workforce"],
    responses={404: {"description": "Not found"}},
)

@router.get("/optimization")
async def get_workforce_optimization(db: Session = Depends(get_db)):
    """
    Get Scientific Workforce Optimization Analysis.
    Calculates Required FTE vs Current FTE based on Standard Time.
    """
    service = WorkforceService(db)
    return service.calculate_optimal_headcount()

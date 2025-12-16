from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database import get_db
from ..services.promotion_service import PromotionService

router = APIRouter(
    prefix="/scientific/promotion",
    tags=["Scientific HR"],
    responses={404: {"description": "Not found"}},
)

service = PromotionService()

@router.get("/simulate")
def simulate_promotion(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Simulates Promotion Scenarios: Tenure vs Growth Slope.
    """
    return service.simulate_promotion(db)

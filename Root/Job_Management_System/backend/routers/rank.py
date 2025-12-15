from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.rank_service import RankService

router = APIRouter(
    prefix="/scientific/rank",
    tags=["Scientific Rank"],
    responses={404: {"description": "Not found"}},
)

@router.get("/list")
async def get_rank_list(db: Session = Depends(get_db)):
    """
    Get the Scientific Promotion Rank List.
    Generated dynamically based on Tenure, Performance Integral, and Growth Slope.
    """
    service = RankService(db)
    return service.generate_rank_list()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.r_and_r_service import RAndRService

router = APIRouter(
    prefix="/job-architecture/r-and-r",
    tags=["Job Architecture"],
    responses={404: {"description": "Not found"}},
)

@router.get("/conflict-map")
async def get_conflict_map(db: Session = Depends(get_db)):
    """
    Get the R&R Conflict Matrix, including Duplication and Gap alerts.
    """
    service = RAndRService(db)
    return service.analyze_conflicts()

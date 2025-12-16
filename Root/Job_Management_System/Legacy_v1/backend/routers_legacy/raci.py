from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.raci_service import RACIService

router = APIRouter(
    prefix="/scientific/raci",
    tags=["Advanced HR Methodologies"],
    responses={404: {"description": "Not found"}},
)

@router.get("/matrix/{process_id}")
async def get_raci_matrix(process_id: str, db: Session = Depends(get_db)):
    """
    Auto-generate RACI Matrix for a specific process (e.g., 'hiring', 'budget').
    """
    service = RACIService(db)
    return service.generate_raci_matrix(process_id)

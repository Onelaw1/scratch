from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.nine_box_service import NineBoxService

router = APIRouter(
    prefix="/scientific/talent",
    tags=["Advanced HR Methodologies"],
    responses={404: {"description": "Not found"}},
)

@router.get("/9-box")
async def get_nine_box_grid(db: Session = Depends(get_db)):
    """
    Get 9-Box Talent Matrix data.
    """
    service = NineBoxService(db)
    return service.generate_grid_data()

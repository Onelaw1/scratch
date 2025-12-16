from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.nine_box_service import NineBoxService

router = APIRouter(
    prefix="/scientific/talent",
    tags=["Advanced HR Methodologies"],
    responses={404: {"description": "Not found"}},
)

from pydantic import BaseModel

class MoveRequest(BaseModel):
    review_id: str
    target_box: int

@router.get("/")
async def get_nine_box_grid(db: Session = Depends(get_db)):
    """
    Get 9-Box Talent Matrix data.
    """
    service = NineBoxService(db)
    return service.get_grid_data()

@router.post("/auto-map")
async def auto_map_employees(db: Session = Depends(get_db)):
    """
    Reset all employees' box positions based on their performance/potential scores.
    """
    service = NineBoxService(db)
    return service.auto_map_all()

@router.post("/move")
async def move_employee(req: MoveRequest, db: Session = Depends(get_db)):
    """
    Manually move an employee to a different box (Calibration).
    """
    service = NineBoxService(db)
    return service.update_box_position(req.review_id, req.target_box)

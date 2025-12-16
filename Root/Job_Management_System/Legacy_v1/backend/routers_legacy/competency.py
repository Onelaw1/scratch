from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.competency_service import CompetencyService
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/scientific/competency",
    tags=["Advanced HR Methodologies"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER'))]
)

@router.get("/radar/{user_id}")
async def get_competency_radar(user_id: str, db: Session = Depends(get_db)):
    """
    Get Competency Fit Radar Chart data (Job vs Person).
    """
    service = CompetencyService(db)
    return service.analyze_fit(user_id)

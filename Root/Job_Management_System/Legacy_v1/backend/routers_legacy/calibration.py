from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database import get_db
from ..services.calibration_service import CalibrationService
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/scientific/calibration",
    tags=["Scientific HR"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN'))]
)

service = CalibrationService()

@router.get("/suggestions")
def get_calibration_suggestions(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Returns data-driven job grade calibration suggestions.
    """
    return service.detect_drift(db)

from fastapi import APIRouter, Depends
from typing import Dict, Any
from ..services.global_service import GlobalService

router = APIRouter(
    prefix="/global",
    tags=["Global Settings"],
    responses={404: {"description": "Not found"}},
)

service = GlobalService()

@router.get("/settings")
def get_global_settings() -> Dict[str, Any]:
    """
    Returns supported currencies and exchange rates.
    """
    return service.get_supported_currencies()

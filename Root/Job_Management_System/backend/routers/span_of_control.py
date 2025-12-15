from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.span_service import SpanService

router = APIRouter(
    prefix="/scientific/org",
    tags=["Advanced HR Methodologies"],
    responses={404: {"description": "Not found"}},
)

@router.get("/span-of-control")
async def get_span_analysis(db: Session = Depends(get_db)):
    """
    Get Organization Span of Control Analysis.
    """
    service = SpanService(db)
    return service.analyze_org_structure()

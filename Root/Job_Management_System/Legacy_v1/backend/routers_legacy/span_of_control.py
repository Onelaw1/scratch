from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.span_service import SpanOfControlService

router = APIRouter(
    prefix="/scientific/org/span-of-control",
    tags=["Scientific HR", "Organization"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def get_span_of_control_tree(db: Session = Depends(get_db)):
    """
    Get Recursive Organizational Tree with Span of Control metrics.
    """
    service = SpanOfControlService(db)
    return service.get_span_of_control_analysis()

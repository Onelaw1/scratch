from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.dynamic_jd_service import DynamicJDService

router = APIRouter(
    prefix="/job-architecture/dynamic-jd",
    tags=["Job Architecture"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{job_id}")
async def analyze_dynamic_jd(job_id: str, db: Session = Depends(get_db)):
    """
    Analyze the drift between Job Description and Workload Logs.
    Returns suggestions to Update (Add/Remove tasks).
    """
    service = DynamicJDService(db)
    return service.analyze_job_drift(job_id)

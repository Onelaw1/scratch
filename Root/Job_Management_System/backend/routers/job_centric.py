from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import sys
import os
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

# Add Root directory to sys.path to allow importing from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Mock NCS Client if not available
try:
    from src.input.ncs_client import NCSClient
except ImportError:
    class NCSClient:
        def search_ncs(self, page=1, per_page=10):
            return {"items": []}

# Mock Analysis Schemas if not available
try:
    from src.analysis.job_schema import JobDescription, JobClassification, JobEvaluation, WorkloadAnalysis
except ImportError:
    from pydantic import BaseModel
    class JobDescription(BaseModel):
        pass
    class JobClassification(BaseModel):
        pass
    class JobEvaluation(BaseModel):
        def calculate_score(self): pass
    class WorkloadAnalysis(BaseModel):
        def calculate_gap(self): pass

from backend.database import get_db
from backend.models import (
    User, JobTask, WorkloadEntry, SurveyPeriod, 
    JobGroup, JobSeries, JobPosition, WorkItem, TaskFrequency,
    Institution, OrgUnit
)
from backend import schemas
from pydantic import BaseModel

router = APIRouter(
    prefix="/job-centric",
    tags=["job-centric"],
    responses={404: {"description": "Not found"}},
)

ncs_client = NCSClient()

@router.get("/ncs/search")
def search_ncs(keyword: Optional[str] = None, page: int = 1, per_page: int = 10):
    """
    Search for NCS Competency Units via the public API.
    """
    data = ncs_client.search_ncs(page=page, per_page=per_page)
    return data

@router.post("/job-description/validate", response_model=JobDescription)
def validate_job_description(jd: JobDescription):
    """
    Validate a Job Description object.
    """
    return jd

@router.post("/job-evaluation/calculate", response_model=JobEvaluation)
def calculate_evaluation(eval_data: JobEvaluation):
    """
    Calculate the total score and grade for a Job Evaluation.
    """
    eval_data.calculate_score()
    return eval_data

@router.post("/workload/analyze", response_model=WorkloadAnalysis)
def analyze_workload(workload: WorkloadAnalysis):
    """
    Analyze workload gap.
    """
    workload.calculate_gap()
    return workload

# --- Job Classification Matrix Endpoints ---

class JobMatrixRowSchema(BaseModel):
    id: Optional[str] = None
    division: Optional[str] = None
    department: Optional[str] = None
    jobGroup: Optional[str] = None
    jobSeries: Optional[str] = None
    ncsCode: Optional[str] = None
    ncsName: Optional[str] = None
    jobPosition: Optional[str] = None
    grade: Optional[str] = None
    tasks: List[str] = []

@router.get("/classification-matrix", response_model=List[JobMatrixRowSchema])
def get_classification_matrix(db: Session = Depends(get_db)):
    """
    Get the Job Classification Matrix data.
    Flattens the hierarchy: User -> Position -> Series -> Group.
    Includes NCS mapping info.
    """
    results = []
    
    # Query Users with their positions
    users = db.query(User).options(
        joinedload(User.job_positions).joinedload(JobPosition.series).joinedload(JobSeries.group),
        joinedload(User.org_unit),
        joinedload(User.job_positions).joinedload(JobPosition.tasks)
    ).all()

    for user in users:
        # If user has no position, show basic info
        if not user.job_positions:
            results.append(JobMatrixRowSchema(
                id=user.id,
                division=user.org_unit.parent.name if user.org_unit and user.org_unit.parent else "-",
                department=user.org_unit.name if user.org_unit else "-",
                jobGroup="-",
                jobSeries="-",
                ncsCode="-",
                ncsName="-",
                jobPosition="-",
                grade="-",
                tasks=[]
            ))
            continue

        # Create a row for each position held by the user
        for pos in user.job_positions:
            results.append(JobMatrixRowSchema(
                id=user.id,
                division=user.org_unit.parent.name if user.org_unit and user.org_unit.parent else "-",
                department=user.org_unit.name if user.org_unit else "-",
                jobGroup=pos.series.group.name if pos.series and pos.series.group else "-",
                jobSeries=pos.series.name if pos.series else "-",
                ncsCode=pos.series.ncs_code if pos.series else "-",
                ncsName=pos.series.ncs_name if pos.series else "-",
                jobPosition=pos.title,
                grade=pos.grade,
                tasks=[t.task_name for t in pos.tasks]
            ))
            
    return results

# --- Workload Survey Endpoints ---

class SurveyTaskSchema(BaseModel):
    id: str
    name: str
    frequency: Optional[str] = None
    hoursPerOccurrence: float = 0.0
    totalHours: float = 0.0

class WorkloadSurveyDataSchema(BaseModel):
    id: str
    name: str
    department: str
    tasks: List[SurveyTaskSchema]
    totalHours: float

@router.get("/workload-survey/{employee_id}", response_model=WorkloadSurveyDataSchema)
def get_workload_survey(employee_id: str, db: Session = Depends(get_db)):
    """
    Get workload survey data for a specific employee.
    """
    user = db.query(User).filter(User.id == employee_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")

    tasks_response = []
    total_hours = 0.0

    # Get assigned tasks via positions
    for pos in user.job_positions:
        for task in pos.tasks:
            # Check if there are work items defined for this task
            work_items = db.query(WorkItem).filter(WorkItem.job_task_id == task.id).all()
            
            if work_items:
                for item in work_items:
                    # Check if there is already an entry for this survey
                    # For simplicity, we just calculate expected hours
                    # In a real scenario, we would join with WorkloadEntry
                    
                    # Calculate annual hours based on frequency
                    freq_multiplier = {
                        TaskFrequency.DAILY: 240,
                        TaskFrequency.WEEKLY: 52,
                        TaskFrequency.MONTHLY: 12,
                        TaskFrequency.YEARLY: 1
                    }.get(item.frequency, 1)
                    
                    calc_hours = item.estimated_hours_per_occurrence * freq_multiplier
                    
                    tasks_response.append(SurveyTaskSchema(
                        id=item.id,
                        name=f"[{task.task_name}] {item.name}",
                        frequency=item.frequency,
                        hoursPerOccurrence=item.estimated_hours_per_occurrence,
                        totalHours=calc_hours
                    ))
                    total_hours += calc_hours
            else:
                # Task without detailed work items
                tasks_response.append(SurveyTaskSchema(
                    id=task.id,
                    name=task.task_name,
                    frequency="IRREGULAR",
                    hoursPerOccurrence=0,
                    totalHours=0
                ))

    return WorkloadSurveyDataSchema(
        id=user.id,
        name=user.name,
        department=user.org_unit.name if user.org_unit else "-",
        tasks=tasks_response,
        totalHours=total_hours
    )

@router.post("/workload-survey/{employee_id}")
def submit_workload_survey(employee_id: str, data: WorkloadSurveyDataSchema, db: Session = Depends(get_db)):
    """
    Submit workload survey data.
    """
    user = db.query(User).filter(User.id == employee_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Clear existing entries for this user (Simplified logic)
    # In production, we should scope this by SurveyPeriod
    db.query(WorkloadEntry).filter(WorkloadEntry.user_id == employee_id).delete()
    
    current_total = 0.0
    new_tasks_response = []

    # Find or create a default survey period
    survey_period = db.query(SurveyPeriod).filter(SurveyPeriod.status == "ACTIVE").first()
    if not survey_period:
        # Create a dummy period if none exists
        # Note: In a real app, this should be managed by admin
        import datetime
        survey_period = SurveyPeriod(
            name="2024 Workload Survey", 
            status="ACTIVE",
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=30)
        )
        db.add(survey_period)
        db.flush()

    for task_data in data.tasks:
        # We assume task_data.id is the WorkItem ID or Task ID
        # Try to find WorkItem first
        work_item = db.query(WorkItem).filter(WorkItem.id == task_data.id).first()
        task_id = None
        
        if work_item:
            task_id = work_item.job_task_id
        else:
            # Try to find JobTask
            job_task = db.query(JobTask).filter(JobTask.id == task_data.id).first()
            if job_task:
                task_id = job_task.id
        
        if task_id:
            # Create WorkloadEntry
            entry = WorkloadEntry(
                survey_period_id=survey_period.id,
                user_id=user.id,
                task_id=task_id,
                standard_time=task_data.totalHours, # Using standard_time to store reported hours
                volume=1 # Default volume
            )
            db.add(entry)
            
        current_total += task_data.totalHours

    db.commit()
    
    return {"message": "Survey submitted successfully", "total_hours": current_total}

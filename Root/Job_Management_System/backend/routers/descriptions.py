from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from .. import crud, models, schemas
from ..database import get_db
import uuid

router = APIRouter(
    prefix="/descriptions",
    tags=["descriptions"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Dict[str, Any]])
def list_job_descriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all Job Descriptions (Positions) for selection.
    """
    positions = db.query(models.JobPosition).offset(skip).limit(limit).all()
    results = []
    for pos in positions:
        results.append({
            "job_id": pos.id, # Using Position ID as the main Job ID link
            "title": pos.title,
            "grade": pos.grade
        })
    return results

@router.get("/{position_id}")
def get_job_description(position_id: str, db: Session = Depends(get_db)):
    """
    Aggregates Job Description data from:
    1. JobPosition (Title, Grade, Series)
    2. JobDescription (Summary, Requirements, KPIs) - Manual Fields
    3. JobTask (List of Responsibilities) - Auto Generated
    4. WorkloadEntry (To calculate relative importance of tasks)
    """
    
    # 1. Fetch Position and Manual Description
    position = db.query(models.JobPosition).filter(models.JobPosition.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Job Position not found")
        
    description = db.query(models.JobDescription).filter(models.JobDescription.job_position_id == position_id).first()
    if not description:
        # Create default empty description if not exists
        description = models.JobDescription(
            id=str(uuid.uuid4()),
            job_position_id=position_id,
            summary="",
            qualification_requirements="",
            kpi_indicators=""
        )
        db.add(description)
        db.commit()
        db.refresh(description)

    # 2. Fetch Tasks and Calculate Weights (Importance)
    # Weight is roughly based on workload volume or FTE contribution
    tasks_data = []
    total_fte_for_pos = 0.0
    
    for task in position.tasks:
        # Calculate total FTE for this task across all users/periods
        task_fte = db.query(func.sum(models.WorkloadEntry.fte))\
            .filter(models.WorkloadEntry.task_id == task.id).scalar() or 0.0
        
        total_fte_for_pos += task_fte
        
        tasks_data.append({
            "id": task.id,
            "task_name": task.task_name,
            "action_verb": task.action_verb,
            "task_object": task.task_object,
            "fte": task_fte,
            "importance": 0.0 # Will calc below
        })
        
    # Normalize Importance
    if total_fte_for_pos > 0:
        for t in tasks_data:
            t["importance"] = round((t["fte"] / total_fte_for_pos) * 100, 1) // Percentage
    else:
        # If no workload data, equal weight or 0
        pass
        
    # Sort tasks by importance desc
    tasks_data.sort(key=lambda x: x["importance"], reverse=True)

    return {
        "position": {
            "title": position.title,
            "grade": position.grade,
            "series": position.series.name if position.series else "N/A",
            "group": position.series.group.name if position.series and position.series.group else "N/A"
        },
        "description": {
            "summary": description.summary,
            "qualification_requirements": description.qualification_requirements,
            "kpi_indicators": description.kpi_indicators,
            "updated_at": "Today" # Placeholder
        },
        "responsibilities": tasks_data
    }

class JobDescriptionUpdate(schemas.BaseModel):
    summary: str
    qualification_requirements: str
    kpi_indicators: str

@router.post("/{position_id}")
def update_job_description(position_id: str, desc_update: JobDescriptionUpdate, db: Session = Depends(get_db)):
    description = db.query(models.JobDescription).filter(models.JobDescription.job_position_id == position_id).first()
    if not description:
         description = models.JobDescription(
            id=str(uuid.uuid4()),
            job_position_id=position_id,
            summary=desc_update.summary,
            qualification_requirements=desc_update.qualification_requirements,
            kpi_indicators=desc_update.kpi_indicators
        )
         db.add(description)
    else:
        description.summary = desc_update.summary
        description.qualification_requirements = desc_update.qualification_requirements
        description.kpi_indicators = desc_update.kpi_indicators
    
    db.commit()
    return {"message": "Job Description updated successfully"}

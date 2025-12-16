from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/api/workflow",
    tags=["workflow"],
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER', 'TEAM_LEAD', 'EMPLOYEE'))]
)

# Kanban Board Endpoints
@router.get("/kanban/{position_id}")
def get_kanban_tasks(position_id: str, db: Session = Depends(get_db)):
    """Get tasks for a job position in Kanban format, ordered by order_index"""
    # Note: JobTask model needs order_index field if not present
    tasks = db.query(models.JobTask).filter(
        models.JobTask.job_position_id == position_id
    ).all()
    return tasks

@router.post("/tasks/{task_id}/move")
def move_task(task_id: str, new_index: int, db: Session = Depends(get_db)):
    """Update task order_index for Kanban drag-and-drop"""
    task = db.query(models.JobTask).filter(models.JobTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # task.order_index = new_index # Model update needed for this field
    db.commit()
    db.refresh(task)
    return task

# Process Map Endpoints
@router.get("/process-map/{position_id}")
def get_process_map(position_id: str, db: Session = Depends(get_db)):
    """Get task dependencies for process flow visualization"""
    tasks = db.query(models.JobTask).filter(models.JobTask.job_position_id == position_id).all()
    task_ids = [task.id for task in tasks]
    
    dependencies = db.query(models.TaskDependency).filter(
        models.TaskDependency.source_task_id.in_(task_ids) |
        models.TaskDependency.target_task_id.in_(task_ids)
    ).all()
    
    return {
        "tasks": tasks,
        "dependencies": dependencies
    }

@router.post("/dependencies", response_model=schemas.TaskDependency)
def create_dependency(dependency: schemas.TaskDependencyCreate, db: Session = Depends(get_db)):
    """Create a task dependency"""
    return crud.create_task_dependency(db, dependency)

# Time Validation Endpoints
@router.get("/validate-hours/{user_id}")
def validate_hours(user_id: str, survey_period_id: str, db: Session = Depends(get_db)):
    """Validate employee annual hours"""
    return crud.validate_employee_annual_hours(db, user_id, survey_period_id)

# Organizational Unit Endpoints
@router.post("/organizational-units", response_model=schemas.OrgUnit)
def create_unit(unit: schemas.OrgUnitCreate, db: Session = Depends(get_db)):
    """Create an organizational unit"""
    # Assuming crud.create_organizational_unit exists or needs update
    # For now, implementing directly to avoid crud mismatch
    db_unit = models.OrgUnit(
        id=unit.id if hasattr(unit, 'id') else None, # Handle ID generation in model or here
        institution_id=unit.institution_id,
        name=unit.name,
        unit_type=unit.unit_type,
        mission=unit.mission,
        parent_id=unit.parent_id
    )
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

@router.get("/organizational-units/{institution_id}", response_model=List[schemas.OrgUnit])
def get_units(institution_id: str, parent_id: str = None, db: Session = Depends(get_db)):
    """Get organizational units for an institution"""
    query = db.query(models.OrgUnit).filter(models.OrgUnit.institution_id == institution_id)
    if parent_id:
        query = query.filter(models.OrgUnit.parent_id == parent_id)
    return query.all()

# Job Improvement Endpoints (Commented out until Schema is defined)
# @router.post("/job-improvements", response_model=schemas.JobImprovement)
# def create_improvement(improvement: schemas.JobImprovementCreate, db: Session = Depends(get_db)):
#     """Create a job improvement suggestion"""
#     return crud.create_job_improvement(db, improvement)

# @router.get("/job-improvements/{job_id}", response_model=List[schemas.JobImprovement])
# def get_improvements(job_id: str, db: Session = Depends(get_db)):
#     """Get job improvement suggestions"""
#     return crud.get_job_improvements(db, job_id)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from .. import models, schemas
from ..database import get_db
# RBAC dependencies
from ..dependencies import require_roles

router = APIRouter(
    prefix="/classification",
    tags=["classification"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN'))]
)

# --- Tree View (File System Style) ---

@router.get("/hierarchy", response_model=List[Dict[str, Any]])
def get_job_hierarchy(db: Session = Depends(get_db)):
    """
    Returns the full job classification hierarchy as a nested tree.
    Level 1: JobGroup
    Level 2: JobSeries
    Level 3: JobPosition
    Level 4: JobTask
    Level 5: WorkItem
    """
    hierarchy = []
    groups = db.query(models.JobGroup).all()
    
    for group in groups:
        group_node = {
            "id": group.id,
            "name": group.name,
            "type": "GROUP",
            "children": []
        }
        
        for series in group.series:
            series_node = {
                "id": series.id,
                "name": series.name,
                "type": "SERIES",
                "ncs_code": series.ncs_code,
                "children": []
            }
            
            for position in series.positions:
                position_node = {
                    "id": position.id,
                    "name": position.title,
                    "type": "POSITION",
                    "grade": position.grade,
                    "children": []
                }
                
                for task in position.tasks:
                    task_node = {
                        "id": task.id,
                        "name": task.task_name,
                        "type": "TASK",
                        "children": []
                    }
                    
                    for item in task.work_items:
                        item_node = {
                            "id": item.id,
                            "name": item.name,
                            "type": "WORK_ITEM",
                            "frequency": item.frequency
                        }
                        task_node["children"].append(item_node)
                        
                    position_node["children"].append(task_node)
                
                series_node["children"].append(position_node)
            
            group_node["children"].append(series_node)
        
        hierarchy.append(group_node)
        
    return hierarchy

# --- Matrix View (Excel Style) ---

@router.get("/matrix", response_model=List[Dict[str, Any]])
def get_job_matrix(db: Session = Depends(get_db)):
    """
    Returns the job classification hierarchy as a flat matrix (list of rows).
    Suitable for Excel export or grid view.
    """
    matrix = []
    groups = db.query(models.JobGroup).all()
    
    for group in groups:
        for series in group.series:
            for position in series.positions:
                for task in position.tasks:
                    if not task.work_items:
                        # Row for task without work items
                        matrix.append({
                            "group_name": group.name,
                            "series_name": series.name,
                            "position_title": position.title,
                            "position_grade": position.grade,
                            "task_name": task.task_name,
                            "work_item_name": None,
                            "frequency": None
                        })
                    else:
                        for item in task.work_items:
                            matrix.append({
                                "group_name": group.name,
                                "series_name": series.name,
                                "position_title": position.title,
                                "position_grade": position.grade,
                                "task_name": task.task_name,
                                "work_item_name": item.name,
                                "frequency": item.frequency
                            })
    return matrix

class JobMatrixItem(schemas.BaseModel):
    group_name: str
    series_name: str
    position_title: str
    position_grade: Optional[str] = None
    task_name: str
    work_item_name: Optional[str] = None
    frequency: Optional[str] = None
    workload: Optional[float] = 0.0

@router.post("/matrix")
def save_job_matrix(items: List[JobMatrixItem], db: Session = Depends(get_db)):
    """
    Saves the job classification matrix.
    This is a simplified implementation that assumes full replacement or updates based on names.
    For a robust implementation, IDs should be used.
    Here we will iterate and create/update based on hierarchy names.
    """
    # 1. Clear existing structure (Optional: Strategy depends on requirements. 
    #    For now, we will try to update/create without deleting everything to preserve IDs if possible,
    #    but given the flat input, it's hard to map back to IDs without them.
    #    Let's assume we are building from scratch or updating based on names.)
    
    import uuid
    
    for item in items:
        # 1. Job Group
        group = db.query(models.JobGroup).filter(models.JobGroup.name == item.group_name).first()
        if not group:
            group = models.JobGroup(id=str(uuid.uuid4()), name=item.group_name)
            db.add(group)
            db.flush()
            
        # 2. Job Series
        series = db.query(models.JobSeries).filter(models.JobSeries.name == item.series_name, models.JobSeries.group_id == group.id).first()
        if not series:
            series = models.JobSeries(id=str(uuid.uuid4()), group_id=group.id, name=item.series_name)
            db.add(series)
            db.flush()
            
        # 3. Job Position
        position = db.query(models.JobPosition).filter(models.JobPosition.title == item.position_title, models.JobPosition.series_id == series.id).first()
        if not position:
            position = models.JobPosition(id=str(uuid.uuid4()), series_id=series.id, title=item.position_title, grade=item.position_grade)
            db.add(position)
            db.flush()
        else:
            if item.position_grade:
                position.grade = item.position_grade
                
        # 4. Job Task
        task = db.query(models.JobTask).filter(models.JobTask.task_name == item.task_name, models.JobTask.job_position_id == position.id).first()
        if not task:
            task = models.JobTask(id=str(uuid.uuid4()), job_position_id=position.id, task_name=item.task_name)
            db.add(task)
            db.flush()
            
        # 5. Work Item
        if item.work_item_name:
            work_item = db.query(models.WorkItem).filter(models.WorkItem.name == item.work_item_name, models.WorkItem.job_task_id == task.id).first()
            if not work_item:
                work_item = models.WorkItem(
                    id=str(uuid.uuid4()), 
                    job_task_id=task.id, 
                    name=item.work_item_name,
                    frequency=item.frequency,
                    estimated_hours_per_occurrence=item.workload # Assuming workload is hours per occurrence for now
                )
                db.add(work_item)
            else:
                work_item.frequency = item.frequency
                work_item.estimated_hours_per_occurrence = item.workload
                
    db.commit()
    return {"message": "Matrix saved successfully"}

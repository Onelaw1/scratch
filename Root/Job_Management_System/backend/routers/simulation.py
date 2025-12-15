from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
import uuid

router = APIRouter(
    prefix="/scenarios",
    tags=["scenarios"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.SimulationScenario)
def create_scenario(scenario: schemas.SimulationScenarioCreate, db: Session = Depends(get_db)):
    db_scenario = models.SimulationScenario(
        id=str(uuid.uuid4()),
        name=scenario.name,
        description=scenario.description
    )
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario

@router.get("/", response_model=List[schemas.SimulationScenario])
def get_scenarios(db: Session = Depends(get_db)):
    return db.query(models.SimulationScenario).all()

@router.post("/{scenario_id}/clone")
def clone_current_state(scenario_id: str, db: Session = Depends(get_db)):
    """
    Clones all current LIVE positions (where scenario_id is NULL) into this scenario.
    It does a deep copy of Positions and their JobTasks.
    """
    scenario = db.query(models.SimulationScenario).filter(models.SimulationScenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    # 1. Fetch Live Positions
    live_positions = db.query(models.JobPosition).filter(models.JobPosition.scenario_id == None).all()
    
    cloned_count = 0
    for pos in live_positions:
        # Clone Position
        new_pos_id = str(uuid.uuid4())
        cloned_pos = models.JobPosition(
            id=new_pos_id,
            series_id=pos.series_id,
            user_id=pos.user_id, # Can keep user assignment or clear it. Keeping for now.
            scenario_id=scenario_id,
            title=pos.title,
            grade=pos.grade,
            is_future_model=True # Scenarios are inherently future/draft models
        )
        db.add(cloned_pos)
        
        # Clone Tasks
        for task in pos.tasks:
            cloned_task = models.JobTask(
                id=str(uuid.uuid4()),
                job_position_id=new_pos_id,
                task_name=task.task_name,
                action_verb=task.action_verb,
                task_object=task.task_object,
                ai_substitution=task.ai_substitution,
                ai_augmentation=task.ai_augmentation,
                ai_generation=task.ai_generation
            )
            db.add(cloned_task)
            
        cloned_count += 1
        
    db.commit()
    return {"message": "Cloned successfully", "positions_count": cloned_count}

@router.get("/{scenario_id}/positions", response_model=List[schemas.JobPosition])
def get_scenario_positions(scenario_id: str, db: Session = Depends(get_db)):
    return db.query(models.JobPosition).filter(models.JobPosition.scenario_id == scenario_id).all()

@router.put("/move-task")
def move_task(move_req: schemas.MoveTaskRequest, db: Session = Depends(get_db)):
    """
    Moves a task from one position to another.
    Both positions must belong to the SAME scenario (or both be live, though moving live tasks is risky).
    """
    task = db.query(models.JobTask).filter(models.JobTask.id == move_req.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    target_pos = db.query(models.JobPosition).filter(models.JobPosition.id == move_req.target_position_id).first()
    if not target_pos:
        raise HTTPException(status_code=404, detail="Target position not found")
    
    # Validation: Ensure positions are in the same scope
    source_pos = task.position
    if source_pos.scenario_id != target_pos.scenario_id:
        raise HTTPException(status_code=400, detail="Cannot move tasks between different scenarios (or Live vs Scenario)")

    task.job_position_id = target_pos.id
    db.commit()
    
    return {"message": "Task moved successfully"}

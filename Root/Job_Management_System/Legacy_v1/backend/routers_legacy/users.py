from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import crud, models, schemas
from ..database import get_db
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN'))]
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

    users = crud.get_users(db, institution_id=institution_id, skip=skip, limit=limit)
    return users

@router.post("/me/pulse", response_model=schemas.PulseCheck)
def create_pulse_check(check: schemas.PulseCheckCreate, db: Session = Depends(get_db)):
    # Mock Auth
    mock_user = db.query(models.User).first()
    if not mock_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Check if already submitted today
    today = date.today()
    existing = db.query(models.PulseCheck).filter(
        models.PulseCheck.user_id == mock_user.id,
        models.PulseCheck.date == today
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already checked in today")
        
    db_check = models.PulseCheck(**check.model_dump(), user_id=mock_user.id)
    db.add(db_check)
    db.commit()
    db.refresh(db_check)
    return db_check

# --- My Job Dashboard (Employee Experience) ---
@router.get("/me/dashboard")
def read_my_dashboard(db: Session = Depends(get_db)):
    # Mock Auth: Get the first user (e.g., 'EMP001') - In prod, use current_user
    mock_user = db.query(models.User).first()
    if not mock_user:
        # Fallback if no data
        return {
            "user": {"name": "Guest", "title": "No User Data", "department": "System"},
            "stats": {"goals_completed": 0, "training_hours": 0, "pulse_score": "N/A"},
            "key_tasks": [],
            "notifications": []
        }
        
    # 1. Job Info
    # User has relationship 'job_positions' (list) or query JobPosition where user_id=user.id
    # Assuming one primary position for now
    job_position = db.query(models.JobPosition).filter(models.JobPosition.user_id == mock_user.id).first()
    
    # 2. Org Info
    org_unit = db.query(models.OrgUnit).filter(models.OrgUnit.id == mock_user.org_unit_id).first()
    dept_name = org_unit.name if org_unit else "Unassigned"
    
    # 3. Stats: Goals
    goal_count = db.query(models.PerformanceGoal)\
        .join(models.PerformanceReview)\
        .filter(models.PerformanceReview.user_id == mock_user.id)\
        .count()
        
    # 4. Stats: Training Hours
    training_hours = 0.0
    completed_trainings = db.query(models.EmployeeTraining)\
        .filter(
            models.EmployeeTraining.user_id == mock_user.id,
            models.EmployeeTraining.status == models.TrainingStatus.COMPLETED
        ).all()
        
    for t in completed_trainings:
        program = db.query(models.TrainingProgram).filter(models.TrainingProgram.id == t.program_id).first()
        if program:
            training_hours += program.duration_hours

    # 5. Pulse Score (Latest Mood)
    today = date.today()
    pulse = db.query(models.PulseCheck).filter(
        models.PulseCheck.user_id == mock_user.id,
        models.PulseCheck.date == today
    ).first()
    
    pulse_display = "N/A"
    if pulse:
        # Map 1-5 to Emojis
        emojis = {1: "😫", 2: "😞", 3: "😐", 4: "🙂", 5: "😁"}
        pulse_display = emojis.get(pulse.mood_score, "🙂")

    # 6. Key Tasks
    tasks = []
    if job_position:
        tasks = db.query(models.JobTask)\
            .filter(models.JobTask.job_position_id == job_position.id)\
            .limit(5).all()

    return {
        "user": {
            "name": mock_user.name,
            "title": job_position.title if job_position else "Unassigned",
            "department": dept_name
        },
        "stats": {
            "goals_completed": goal_count,
            "training_hours": round(training_hours, 1),
            "pulse_score": pulse_display
        },
        "key_tasks": [t.task_name for t in tasks],
        "notifications": [
            {"id": 1, "text": "Annual survey due in 3 days", "type": "warning"},
            {"id": 2, "text": "New Python training available", "type": "info"}
        ]
    }

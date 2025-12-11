from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .. import crud, models
from ..database import get_db
import os

router = APIRouter(
    prefix="/web",
    tags=["web"],
    include_in_schema=False
)

@router.get("/", response_class=HTMLResponse)
def view_home(request: Request):
    return templates.TemplateResponse("index_v4.html", {"request": request})

@router.get("/performance-review", response_class=HTMLResponse)
def view_performance_review(request: Request):
    return templates.TemplateResponse("performance_review.html", {"request": request})

@router.get("/training-management", response_class=HTMLResponse)
def view_training_management(request: Request):
    return templates.TemplateResponse("training_management.html", {"request": request})

@router.get("/job-record-card", response_class=HTMLResponse)
def view_job_record_card(request: Request):
    return templates.TemplateResponse("job_record_card.html", {"request": request})

# Setup Templates
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/jobs", response_class=HTMLResponse)
def view_jobs(request: Request, db: Session = Depends(get_db)):
    # For demo, get the first institution or use a dummy ID
    # In real app, this would come from session/auth
    institution = db.query(models.Institution).first()
    if not institution:
        # Create dummy institution for demo if empty
        institution = models.Institution(
            name="Demo Public Corp", 
            code="DEMO001", 
            category_type="MARKET", 
            evaluation_group="SOC"
        )
        db.add(institution)
        db.commit()
    
    jobs = crud.get_jobs(db, institution.id)
    return templates.TemplateResponse("job_analysis.html", {"request": request, "jobs": jobs, "institution": institution})

@router.get("/dashboard", response_class=HTMLResponse)
def view_dashboard(request: Request, db: Session = Depends(get_db)):
    institution = db.query(models.Institution).first()
    # Dummy stats for demo
    stats = {
        "management_ratio": 12.5,
        "it_ratio": 5.2,
        "revenue_per_head": 520000000
    }
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "stats": stats, 
        "institution_id": institution.id if institution else "demo"
    })

@router.get("/classification", response_class=HTMLResponse)
def view_classification(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("classification.html", {"request": request})

@router.get("/workload-survey", response_class=HTMLResponse)
def view_workload_survey(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("workload_survey.html", {"request": request})

@router.get("/task-listing", response_class=HTMLResponse)
def view_task_listing(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("task_listing.html", {"request": request})

@router.get("/job-classification", response_class=HTMLResponse)
def view_job_classification(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("job_classification_matrix.html", {"request": request})

@router.get("/my-workflow", response_class=HTMLResponse)
def view_my_workflow(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("my_workflow.html", {"request": request})

@router.get("/workload", response_class=HTMLResponse)
def view_workload(request: Request, db: Session = Depends(get_db)):
    # Placeholder for workload page
    return templates.TemplateResponse("workload_survey.html", {"request": request})

@router.get("/career-map", response_class=HTMLResponse)
def view_career_map(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("career_map.html", {"request": request})

@router.get("/info-architecture", response_class=HTMLResponse)
def view_info_architecture(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("info_architecture.html", {"request": request})

@router.get("/job-description-editor", response_class=HTMLResponse)
def view_job_description_editor(request: Request):
    return templates.TemplateResponse("job_description_editor.html", {"request": request})

@router.get("/job-evaluation", response_class=HTMLResponse)
def view_job_evaluation(request: Request):
    return templates.TemplateResponse("job_evaluation.html", {"request": request})

@router.get("/proposal-slides", response_class=HTMLResponse)
def view_proposal_slides(request: Request):
    return templates.TemplateResponse("proposal_slides.html", {"request": request})


from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    institutions, jobs, surveys, statistics, workflow, 
    organization, tasks, frontend, job_centric, strategy, 
    reporting, job_analysis, ai_impact, evaluation, performance, users, training, workforce, classification, productivity,
    simulation, descriptions, personnel, career, ai, erp, wage, compliance, fairness, prediction, global_settings, blockchain, calibration, integral, promotion, rank, workforce_optimization, dynamic_jd, r_and_r, raci, nine_box, span_of_control, competency
)
from .database import engine, Base

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Public Institution HR Platform API",
    description="API for Job Management, AI Analysis, and HR Evaluation",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Next.js Frontend
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(institutions.router)
app.include_router(jobs.router)
app.include_router(surveys.router)
app.include_router(statistics.router)
app.include_router(workflow.router)
app.include_router(organization.router)
app.include_router(tasks.router)
app.include_router(frontend.router)
app.include_router(job_centric.router)
app.include_router(strategy.router)
app.include_router(performance.router)
app.include_router(training.router)
app.include_router(users.router)
app.include_router(reporting.router)
app.include_router(job_analysis.router)
app.include_router(ai_impact.router)
app.include_router(evaluation.router)
app.include_router(workforce.router)
app.include_router(classification.router)
app.include_router(productivity.router)
app.include_router(simulation.router)
app.include_router(personnel.router)
app.include_router(career.router)
app.include_router(ai.router)
app.include_router(erp.router)
app.include_router(wage.router)
app.include_router(wage.router)
app.include_router(compliance.router)
app.include_router(fairness.router)
app.include_router(prediction.router)
app.include_router(global_settings.router)
app.include_router(blockchain.router)
app.include_router(calibration.router)
app.include_router(integral.router)
app.include_router(promotion.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Public Institution HR Platform API"}

@app.get("/web", include_in_schema=False)
def web_root(request: Request):
    from fastapi.templating import Jinja2Templates
    import os
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    templates = Jinja2Templates(directory=templates_dir)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/web/report", include_in_schema=False)
def web_report(request: Request):
    from fastapi.templating import Jinja2Templates
    import os
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    templates = Jinja2Templates(directory=templates_dir)
    return templates.TemplateResponse("report_generation.html", {"request": request})

@app.get("/web/job-classification-matrix", include_in_schema=False)
def web_job_classification_matrix(request: Request):
    from fastapi.templating import Jinja2Templates
    import os
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    templates = Jinja2Templates(directory=templates_dir)
    return templates.TemplateResponse("job_classification_matrix.html", {"request": request})

@app.get("/health")
def health_check():
    return {"status": "healthy"}

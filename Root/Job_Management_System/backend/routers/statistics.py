from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/export/excel/{institution_id}")
def export_excel(institution_id: str, db: Session = Depends(get_db)):
    # Fetch data
    institution = crud.get_institution(db, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    
    jobs = crud.get_jobs(db, institution_id)
    surveys = crud.get_survey_periods(db, institution_id)
    
    # Prepare DataFrames
    data_jobs = []
    for job in jobs:
        for task in job.tasks:
            data_jobs.append({
                "Job Title": job.title,
                "Task Name": task.task_name,
                "Frequency": task.frequency,
                "Difficulty": task.difficulty,
                "Importance": task.importance
            })
    
    df_jobs = pd.DataFrame(data_jobs)
    
    # Create Excel in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_jobs.to_excel(writer, sheet_name='Job Analysis', index=False)
        # Add more sheets for Workload, Evaluation, etc.
    
    output.seek(0)
    
    headers = {
        'Content-Disposition': f'attachment; filename="{institution.name}_export.xlsx"'
    }
    return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@router.get("/dashboard/{institution_id}")
def get_dashboard_stats(institution_id: str, db: Session = Depends(get_db)):
    # Placeholder for dashboard stats logic
    return {
        "management_ratio": 12.5,
        "it_ratio": 5.2,
        "revenue_per_head": 520000000
    }

@router.get("/reports/job-distribution/{institution_id}")
def generate_job_distribution_report(institution_id: str, db: Session = Depends(get_db)):
    from ..services.report_service import ReportService
    from fastapi.responses import FileResponse
    import os
    
    service = ReportService()
    chart_path = service.generate_job_distribution_chart(db, institution_id)
    
    if not chart_path or not os.path.exists(chart_path):
        raise HTTPException(status_code=404, detail="Could not generate chart or no data available")
        
    return FileResponse(chart_path)

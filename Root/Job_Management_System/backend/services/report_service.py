import sys
import os
from typing import Dict, List
from sqlalchemy.orm import Session
from .. import models

# Add Root directory to sys.path to import from PPT_Agent
# Assuming Root is 3 levels up from this file (backend/services/report_service.py)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(ROOT_DIR)

try:
    from PPT_Agent.src.services.chart_service import ChartService
except ImportError:
    print("Warning: Could not import ChartService from PPT_Agent. Charts will not be generated.")
    ChartService = None

class ReportService:
    def __init__(self, output_dir: str = "backend/static/charts"):
        self.output_dir = output_dir
        if ChartService:
            self.chart_service = ChartService(output_dir=self.output_dir)
        else:
            self.chart_service = None

    def generate_job_distribution_chart(self, db: Session, institution_id: str) -> str:
        """
        Generates a bar chart showing the number of jobs per department.
        Returns the path to the generated image.
        """
        if not self.chart_service:
            return None

        # Fetch data: Count jobs per department
        departments = db.query(models.Department).filter(models.Department.institution_id == institution_id).all()
        data = {}
        for dept in departments:
            job_count = db.query(models.Job).filter(models.Job.department_id == dept.id).count()
            if job_count > 0:
                data[dept.name] = float(job_count)

        if not data:
            return None

        filename = f"job_dist_{institution_id}.png"
        return self.chart_service.generate_bar_chart(
            data=data,
            title="Job Distribution by Department",
            filename=filename
        )

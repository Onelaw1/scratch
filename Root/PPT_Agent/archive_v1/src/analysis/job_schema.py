from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

# --- NCS Data Models ---

class NCSCompetencyElement(BaseModel):
    element_name: str
    performance_criteria: List[str] = []
    knowledge: List[str] = []
    skills: List[str] = []

class NCSCompetencyUnit(BaseModel):
    ncs_code: str
    unit_name: str
    unit_definition: Optional[str] = None
    elements: List[NCSCompetencyElement] = []

# --- Job Classification ---

class JobClassification(BaseModel):
    department: str
    team: str
    job_code: str
    job_name: str
    job_family: Optional[str] = None
    
# --- Job Description ---

class Task(BaseModel):
    task_name: str
    frequency: Literal["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "Ad-hoc"]
    time_per_occurrence: float = Field(..., description="Hours per occurrence")
    volume: float = Field(..., description="Number of occurrences per frequency period")
    total_hours_per_year: float = Field(..., description="Calculated total hours per year")

class JobDescription(BaseModel):
    classification: JobClassification
    purpose: str
    key_responsibilities: List[str] = []
    kpis: List[str] = []
    competencies: List[str] = []
    tasks: List[Task] = []
    ncs_references: List[NCSCompetencyUnit] = []
    
    def calculate_total_workload(self) -> float:
        return sum(task.total_hours_per_year for task in self.tasks)

# --- Job Evaluation ---

class JobEvaluation(BaseModel):
    job_code: str
    know_how_score: int = 0
    problem_solving_score: int = 0
    accountability_score: int = 0
    total_score: int = 0
    grade: Optional[str] = None
    
    def calculate_score(self):
        self.total_score = self.know_how_score + self.problem_solving_score + self.accountability_score
        # Simple grading logic (placeholder)
        if self.total_score > 500:
            self.grade = "A"
        elif self.total_score > 300:
            self.grade = "B"
        else:
            self.grade = "C"

# --- Workload Analysis ---

class WorkloadAnalysis(BaseModel):
    job_code: str
    current_fte: float
    required_fte: float
    industry_average_fte: Optional[float] = None
    gap: float = 0.0
    
    def calculate_gap(self):
        self.gap = self.required_fte - self.current_fte

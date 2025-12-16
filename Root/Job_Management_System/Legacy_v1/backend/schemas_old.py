from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from enum import Enum

# --- Enums ---
class UnitType(str, Enum):
    HQ = "HQ"
    OFFICE = "OFFICE"
    TEAM = "TEAM"

class JobGrade(str, Enum):
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    G5 = "G5"

class InstitutionCategory(str, Enum):
    MARKET = "MARKET"
    QUASI_MARKET = "QUASI_MARKET"
    FUND = "FUND"
    CONSIGNMENT = "CONSIGNMENT"

class SurveyStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class DependencyType(str, Enum):
    BLOCKS = "BLOCKS"
    RELATED = "RELATED"
    SEQUENTIAL = "SEQUENTIAL"

class TaskFrequency(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    SEASONAL = "SEASONAL"
    IRREGULAR = "IRREGULAR"

# --- Base Schemas ---
class InstitutionBase(BaseModel):
    name: str
    code: str
    category: Optional[InstitutionCategory] = None

class InstitutionCreate(InstitutionBase):
    pass

class Institution(InstitutionBase):
    id: str

    class Config:
        from_attributes = True

class OrgUnitBase(BaseModel):
    name: str
    unit_type: UnitType
    mission: Optional[str] = None
    parent_id: Optional[str] = None

class OrgUnitCreate(OrgUnitBase):
    institution_id: str

class OrgUnit(OrgUnitBase):
    id: str
    institution_id: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    name: str
    hire_date: Optional[date] = None

class UserCreate(UserBase):
    institution_id: str
    org_unit_id: str

class User(UserBase):
    id: str
    institution_id: str
    org_unit_id: str

    class Config:
        from_attributes = True

# --- Strategic Analysis Schemas ---
class StrategicAnalysisBase(BaseModel):
    institution_id: str
    analysis_type: str
    content: str # JSON string

class StrategicAnalysisCreate(StrategicAnalysisBase):
    pass

class StrategicAnalysisUpdate(BaseModel):
    content: Optional[str] = None

class StrategicAnalysis(StrategicAnalysisBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Job Schemas ---
class JobBase(BaseModel):
    title: str
    description: Optional[str] = None

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: str
    institution_id: str

    class Config:
        from_attributes = True

class JobGroupBase(BaseModel):
    name: str

class JobGroupCreate(JobGroupBase):
    id: Optional[str] = None

class JobGroupUpdate(JobGroupBase):
    pass

class JobGroup(JobGroupBase):
    id: str
    # series: List["JobSeries"] = [] # Forward ref issue, omitting for now or use string

    class Config:
        from_attributes = True

class JobSeriesBase(BaseModel):
    name: str

class JobSeriesCreate(JobSeriesBase):
    id: Optional[str] = None
    group_id: str

class JobSeriesUpdate(JobSeriesBase):
    pass

class JobSeries(JobSeriesBase):
    id: str
    group_id: str
    class Config:
        from_attributes = True

class JobPositionBase(BaseModel):
    title: str
    grade: Optional[JobGrade] = None
    is_future_model: bool = False

class JobPositionCreate(JobPositionBase):
    id: Optional[str] = None
    series_id: str

class JobPositionUpdate(JobPositionBase):
    pass

class JobPosition(JobPositionBase):
    id: str
    series_id: str

    class Config:
        from_attributes = True

class JobTaskBase(BaseModel):
    task_name: str
    action_verb: Optional[str] = None
    task_object: Optional[str] = None
    ai_substitution: float = 0.0
    ai_augmentation: float = 0.0
    ai_generation: float = 0.0

class JobTaskCreate(JobTaskBase):
    id: Optional[str] = None
    position_id: str

class JobTaskUpdate(JobTaskBase):
    pass

class JobTask(JobTaskBase):
    id: str
    position_id: str

    class Config:
        from_attributes = True

# --- Survey & Workload Schemas ---
class SurveyPeriodBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    status: SurveyStatus = SurveyStatus.DRAFT

class SurveyPeriodCreate(SurveyPeriodBase):
    pass

class SurveyPeriod(SurveyPeriodBase):
    id: str
    institution_id: str

    class Config:
        from_attributes = True

class WorkloadEntryBase(BaseModel):
    volume: float
    standard_time: float

class WorkloadEntryCreate(WorkloadEntryBase):
    user_id: str
    task_id: str
    survey_period_id: Optional[str] = None

class WorkloadEntry(WorkloadEntryBase):
    id: str
    user_id: str
    task_id: str
    fte: float
    survey_period_id: Optional[str] = None

    class Config:
        from_attributes = True

class ExternalBenchmarkDataBase(BaseModel):
    institution_type: str
    headcount_range: str
    budget_range: str
    avg_hcroi: float
    avg_hcva: float

class ExternalBenchmarkDataCreate(ExternalBenchmarkDataBase):
    institution_id: Optional[str] = None

class ExternalBenchmarkData(ExternalBenchmarkDataBase):
    id: str
    institution_id: Optional[str] = None

    class Config:
        from_attributes = True

# --- Workflow & Task Management Schemas ---
class TaskDependencyBase(BaseModel):
    dependency_type: DependencyType
    description: Optional[str] = None

class TaskDependencyCreate(TaskDependencyBase):
    source_task_id: str
    target_task_id: str

class TaskDependency(TaskDependencyBase):
    id: str
    source_task_id: str
    target_task_id: str

    class Config:
        from_attributes = True

class WorkItemBase(BaseModel):
    name: str
    code: Optional[str] = None
    frequency: Optional[TaskFrequency] = None
    seasonal_details: Optional[str] = None
    estimated_hours_per_occurrence: Optional[float] = None
    workload_amount: Optional[float] = None

class WorkItemCreate(WorkItemBase):
    job_task_id: str

class WorkItemUpdate(WorkItemBase):
    pass

class WorkItem(WorkItemBase):
    id: str
    job_task_id: str

    class Config:
        from_attributes = True

# --- Phase 3: Job Evaluation Schemas ---
class RaterType(str, Enum):
    SELF = "SELF"
    PEER = "PEER"
    SUPERVISOR_1 = "SUPERVISOR_1"
    SUPERVISOR_2 = "SUPERVISOR_2"
    EXTERNAL = "EXTERNAL"

class JobEvaluationScoreBase(BaseModel):
    rater_type: RaterType
    score_expertise: float
    score_responsibility: float
    score_complexity: float
    rater_user_id: Optional[str] = None

class JobEvaluationScoreCreate(JobEvaluationScoreBase):
    evaluation_id: Optional[str] = None

class JobEvaluationScore(JobEvaluationScoreBase):
    id: str
    evaluation_id: str
    raw_total: float
    z_score: float
    final_score: float

    class Config:
        from_attributes = True

class JobEvaluationBase(BaseModel):
    job_position_id: str
    grade: Optional[JobGrade] = None

class JobEvaluationCreate(JobEvaluationBase):
    pass

class JobEvaluation(JobEvaluationBase):
    id: str
    total_score: float
    scores: List[JobEvaluationScore] = []

    class Config:
        from_attributes = True

# --- Phase 4: Performance Evaluation Schemas ---
class ReviewStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    FINAL = "FINAL"

class PerformanceGoalBase(BaseModel):
    category: str
    goal_text: str
    weight: float
    target: Optional[str] = None
    actual: Optional[str] = None
    self_score: float = 0.0
    supervisor_score: float = 0.0

class PerformanceGoalCreate(PerformanceGoalBase):
    review_id: Optional[str] = None

class PerformanceGoalUpdate(BaseModel):
    category: Optional[str] = None
    goal_text: Optional[str] = None
    weight: Optional[float] = None
    target: Optional[str] = None
    actual: Optional[str] = None
    self_score: Optional[float] = None
    supervisor_score: Optional[float] = None
    final_score: Optional[float] = None

class PerformanceGoal(PerformanceGoalBase):
    id: str
    review_id: str
    final_score: float

    class Config:
        from_attributes = True

class PerformanceReviewBase(BaseModel):
    user_id: str
    year: int
    status: ReviewStatus = ReviewStatus.DRAFT
    review_date: Optional[date] = None
    score_common: float = 0.0
    score_leadership: float = 0.0

class PerformanceReviewCreate(PerformanceReviewBase):
    pass

class PerformanceReviewUpdate(BaseModel):
    status: Optional[ReviewStatus] = None
    review_date: Optional[date] = None
    score_common: Optional[float] = None
    score_leadership: Optional[float] = None
    score_job: Optional[float] = None
    total_score: Optional[float] = None
    grade: Optional[str] = None

class PerformanceReview(PerformanceReviewBase):
    id: str
    score_job: float
    total_score: float
    grade: Optional[str] = None
    goals: List[PerformanceGoal] = []

    class Config:
        from_attributes = True

# --- Phase 4: Training Management Schemas ---
class TrainingStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class TrainingProgramBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration_hours: float = 0.0
    target_job_series_id: Optional[str] = None
    required_competency: Optional[str] = None

class TrainingProgramCreate(TrainingProgramBase):
    pass

class TrainingProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_hours: Optional[float] = None
    target_job_series_id: Optional[str] = None
    required_competency: Optional[str] = None

class TrainingProgram(TrainingProgramBase):
    id: str

    class Config:
        from_attributes = True

class EmployeeTrainingBase(BaseModel):
    user_id: str
    program_id: str
    status: TrainingStatus = TrainingStatus.PLANNED
    completion_date: Optional[date] = None
    score: Optional[float] = None

class EmployeeTrainingCreate(EmployeeTrainingBase):
    pass

class EmployeeTrainingUpdate(BaseModel):
    status: Optional[TrainingStatus] = None
    completion_date: Optional[date] = None
    score: Optional[float] = None

class EmployeeTraining(EmployeeTrainingBase):
    id: str
    program: TrainingProgram

    class Config:
        from_attributes = True

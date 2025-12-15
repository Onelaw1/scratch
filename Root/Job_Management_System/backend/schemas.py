from pydantic import BaseModel
from typing import List, Optional, Dict, Any
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

class TrainingStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class ReviewStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    FINAL = "FINAL"

class RaterType(str, Enum):
    SELF = "SELF"
    PEER = "PEER"
    SUPERVISOR_1 = "SUPERVISOR_1"
    SUPERVISOR_2 = "SUPERVISOR_2"
    EXTERNAL = "EXTERNAL"

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

# --- Productivity ---
class FinancialPerformanceBase(BaseModel):
    year: int
    revenue: float
    operating_expenses: float
    personnel_costs: float

class FinancialPerformanceCreate(FinancialPerformanceBase):
    institution_id: str

class FinancialPerformance(FinancialPerformanceBase):
    id: str
    institution_id: str
    net_income: float
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
    birth_date: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    education_level: Optional[str] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    career_history: Optional[List[Dict[str, Any]]] = None
    reports_to_id: Optional[str] = None

class UserCreate(UserBase):
    institution_id: str
    org_unit_id: str

class User(UserBase):
    id: str
    institution_id: str
    org_unit_id: str
    reports_to_id: Optional[str] = None
    class Config:
        from_attributes = True

# --- Job Architecture ---
class JobGroupBase(BaseModel):
    name: str

class JobGroupCreate(JobGroupBase):
    pass

class JobGroup(JobGroupBase):
    id: str
    class Config:
        from_attributes = True

class JobSeriesBase(BaseModel):
    name: str
    ncs_code: Optional[str] = None
    ncs_name: Optional[str] = None

class JobSeriesCreate(JobSeriesBase):
    group_id: str

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
    series_id: str

class JobPosition(JobPositionBase):
    id: str
    series_id: str
    scenario_id: Optional[str] = None
    class Config:
        from_attributes = True

# --- Job Redesign (Simulation) ---
class SimulationScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None

class SimulationScenarioCreate(SimulationScenarioBase):
    pass

class SimulationScenario(SimulationScenarioBase):
    id: str
    created_at: datetime
    # positions: related items omitted for brevity
    class Config:
        from_attributes = True

class MoveTaskRequest(BaseModel):
    task_id: str
    target_position_id: str

class JobTaskBase(BaseModel):
    task_name: str
    action_verb: Optional[str] = None
    task_object: Optional[str] = None
    ai_substitution: float = 0.0
    ai_augmentation: float = 0.0
    ai_generation: float = 0.0

class JobTaskCreate(JobTaskBase):
    job_position_id: str

class JobTask(JobTaskBase):
    id: str
    job_position_id: str
    class Config:
        from_attributes = True

# --- 2.12 Competency ---
class CompetencyBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class CompetencyCreate(CompetencyBase):
    pass

class Competency(CompetencyBase):
    id: str
    class Config:
        from_attributes = True

class JobCompetencyBase(BaseModel):
    required_level: int = 1
    weight: float = 1.0

class JobCompetencyCreate(JobCompetencyBase):
    job_position_id: str
    competency_id: str

class JobCompetency(JobCompetencyBase):
    id: str
    job_position_id: str
    competency_id: str
    competency: Optional[Competency] = None 
    class Config:
        from_attributes = True

class UserCompetencyBase(BaseModel):
    current_level: int = 1

class UserCompetencyCreate(UserCompetencyBase):
    user_id: str
    competency_id: str

class UserCompetency(UserCompetencyBase):
    id: str
    user_id: str
    competency_id: str
    competency: Optional[Competency] = None
    evaluated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# --- Workload & Survey ---
class SurveyPeriodBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    status: SurveyStatus = SurveyStatus.DRAFT

class SurveyPeriodCreate(SurveyPeriodBase):
    institution_id: str

class SurveyPeriod(SurveyPeriodBase):
    id: str
    institution_id: str
    class Config:
        from_attributes = True

class WorkloadEntryBase(BaseModel):
    volume: float
    standard_time: float
    fte: Optional[float] = None

class WorkloadEntryCreate(WorkloadEntryBase):
    user_id: str
    task_id: str
    survey_period_id: Optional[str] = None

class WorkloadEntry(WorkloadEntryBase):
    id: str
    user_id: str
    task_id: str
    survey_period_id: Optional[str] = None
    class Config:
        from_attributes = True

# --- Headcount Management ---
class HeadcountPlanBase(BaseModel):
    year: int
    authorized_count: float
    current_count: float
    required_count: float

class HeadcountPlanCreate(HeadcountPlanBase):
    institution_id: str
    org_unit_id: Optional[str] = None

class HeadcountPlan(HeadcountPlanBase):
    id: str
    institution_id: str
    org_unit_id: Optional[str] = None
    class Config:
        from_attributes = True

# --- Job Evaluation ---
class JobEvaluationBase(BaseModel):
    score_expertise: float
    score_responsibility: float
    score_complexity: float
    total_score: float
    grade: Optional[JobGrade] = None

class JobEvaluationCreate(JobEvaluationBase):
    job_position_id: str

class JobEvaluation(JobEvaluationBase):
    id: str
    job_position_id: str
    class Config:
        from_attributes = True

# --- Performance Review ---
class PerformanceReviewBase(BaseModel):
    year: int
    status: ReviewStatus = ReviewStatus.DRAFT
    review_date: Optional[date] = None
    score_common: float = 0.0
    score_leadership: float = 0.0
    score_job: float = 0.0
    total_score: float = 0.0
    grade: Optional[str] = None

class PerformanceReviewCreate(PerformanceReviewBase):
    user_id: str

class PerformanceReview(PerformanceReviewBase):
    id: str
    user_id: str
    class Config:
        from_attributes = True

# --- Promotion ---
class PromotionListBase(BaseModel):
    target_grade: JobGrade
    rank: int
    total_points: float
    score_performance: float = 0.0
    score_experience: float = 0.0
    score_language: float = 0.0
    score_training: float = 0.0

class PromotionListCreate(PromotionListBase):
    user_id: str

class PromotionList(PromotionListBase):
    id: str
    user_id: str
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

# --- Missing Update Schemas ---

class JobGroupUpdate(BaseModel):
    name: Optional[str] = None

class JobSeriesUpdate(BaseModel):
    name: Optional[str] = None
    ncs_code: Optional[str] = None
    ncs_name: Optional[str] = None

class JobPositionUpdate(BaseModel):
    title: Optional[str] = None
    grade: Optional[JobGrade] = None
    is_future_model: Optional[bool] = None

class JobTaskUpdate(BaseModel):
    task_name: Optional[str] = None
    action_verb: Optional[str] = None
    task_object: Optional[str] = None
    ai_substitution: Optional[float] = None
    ai_augmentation: Optional[float] = None
    ai_generation: Optional[float] = None

class WorkItemUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[TaskFrequency] = None
    seasonal_details: Optional[str] = None
    estimated_hours_per_occurrence: Optional[float] = None
    workload_amount: Optional[float] = None

class StrategicAnalysisUpdate(BaseModel):
    analysis_type: Optional[str] = None
    content: Optional[str] = None

# --- Missing WorkItem Schemas ---

class WorkItemBase(BaseModel):
    name: str
    code: Optional[str] = None
    frequency: Optional[TaskFrequency] = None
    seasonal_details: Optional[str] = None
    estimated_hours_per_occurrence: Optional[float] = None
    workload_amount: Optional[float] = None

class WorkItemCreate(WorkItemBase):
    job_task_id: str

class WorkItem(WorkItemBase):
    id: str
    job_task_id: str

    class Config:
        from_attributes = True

# --- Missing Strategic Analysis Schemas ---

class StrategicAnalysisBase(BaseModel):
    institution_id: str
    analysis_type: str
    content: str # JSON string

class StrategicAnalysisCreate(StrategicAnalysisBase):
    pass

class StrategicAnalysis(StrategicAnalysisBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Missing Job Evaluation Schemas ---

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

# --- Missing Performance Review Schemas ---

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
    score_potential: float = 0.0

class PerformanceReviewCreate(PerformanceReviewBase):
    pass

class PerformanceReviewUpdate(BaseModel):
    status: Optional[ReviewStatus] = None
    review_date: Optional[date] = None
    score_common: Optional[float] = None
    score_leadership: Optional[float] = None
    score_job: Optional[float] = None
    score_potential: Optional[float] = None
    total_score: Optional[float] = None
    grade: Optional[str] = None
    potential_grade: Optional[str] = None
    nine_box_position: Optional[int] = None

class PerformanceReview(PerformanceReviewBase):
    id: str
    score_job: float
    score_potential: float
    total_score: float
    grade: Optional[str] = None
    potential_grade: Optional[str] = None
    nine_box_position: Optional[int] = None
    goals: List[PerformanceGoal] = []

    class Config:
        from_attributes = True

# --- Missing Training Schemas ---

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
    # program: TrainingProgram # Forward ref issue, omitting for now

    class Config:
        from_attributes = True

# --- Missing Promotion Schemas ---

class PromotionListBase(BaseModel):
    target_grade: JobGrade
    rank: int
    total_points: float
    score_performance: float = 0.0
    score_experience: float = 0.0
    score_language: float = 0.0
    score_training: float = 0.0

class PromotionListCreate(PromotionListBase):
    user_id: str

class PromotionList(PromotionListBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True

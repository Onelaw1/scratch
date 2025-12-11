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

class UserCreate(UserBase):
    institution_id: str
    org_unit_id: str

class User(UserBase):
    id: str
    institution_id: str
    org_unit_id: str
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
    job_position_id: str

class JobTask(JobTaskBase):
    id: str
    job_position_id: str
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
    fte: float

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

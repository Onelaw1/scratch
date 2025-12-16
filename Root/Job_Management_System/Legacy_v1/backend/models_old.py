from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Text, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid
import enum

def generate_uuid():
    return str(uuid.uuid4())

# --- Enums ---
class InstitutionCategory(str, enum.Enum):
    MARKET = "MARKET"
    QUASI_MARKET = "QUASI_MARKET"
    FUND = "FUND"
    CONSIGNMENT = "CONSIGNMENT"

class UnitType(str, enum.Enum):
    HQ = "HQ"          # 본부
    OFFICE = "OFFICE"  # 실
    TEAM = "TEAM"      # 팀

class JobGrade(str, enum.Enum):
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    G5 = "G5"

class SurveyStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class DependencyType(str, enum.Enum):
    BLOCKS = "BLOCKS"
    RELATED = "RELATED"
    SEQUENTIAL = "SEQUENTIAL"

class TaskFrequency(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    SEASONAL = "SEASONAL"
    IRREGULAR = "IRREGULAR"

class RaterType(str, enum.Enum):
    SELF = "SELF"
    PEER = "PEER"
    SUPERVISOR_1 = "SUPERVISOR_1" # Direct
    SUPERVISOR_2 = "SUPERVISOR_2" # Next Level
    EXTERNAL = "EXTERNAL" # Committee

class ReviewStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    FINAL = "FINAL"

class TrainingStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

# --- Core Models ---
class Institution(Base):
    __tablename__ = "institutions"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    category = Column(Enum(InstitutionCategory), nullable=True)
    
    org_units = relationship("OrgUnit", back_populates="institution")
    users = relationship("User", back_populates="institution")
    benchmark_data = relationship("ExternalBenchmarkData", back_populates="institution")
    strategic_analyses = relationship("StrategicAnalysis", back_populates="institution")

class OrgUnit(Base):
    __tablename__ = "org_units"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    parent_id = Column(String, ForeignKey("org_units.id"), nullable=True)
    name = Column(String, nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False)
    mission = Column(Text, nullable=True) # For Cascading
    
    institution = relationship("Institution", back_populates="org_units")
    parent = relationship("OrgUnit", remote_side=[id], backref="children")
    users = relationship("User", back_populates="org_unit")
    team_budgets = relationship("TeamBudget", back_populates="org_unit")

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    org_unit_id = Column(String, ForeignKey("org_units.id"))
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hire_date = Column(Date, nullable=True)
    
    institution = relationship("Institution", back_populates="users")
    org_unit = relationship("OrgUnit", back_populates="users")
    job_positions = relationship("JobPosition", back_populates="user")

# --- Strategic Analysis ---
class StrategicAnalysis(Base):
    __tablename__ = "strategic_analyses"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    analysis_type = Column(String, nullable=False) # PEST, SWOT, etc.
    content = Column(Text, nullable=False) # JSON string
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    institution = relationship("Institution", back_populates="strategic_analyses")

# --- Job Architecture ---
class JobGroup(Base):
    __tablename__ = "job_groups"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    series = relationship("JobSeries", back_populates="group")

class JobSeries(Base):
    __tablename__ = "job_series"
    id = Column(String, primary_key=True, default=generate_uuid)
    group_id = Column(String, ForeignKey("job_groups.id"))
    name = Column(String, nullable=False)
    group = relationship("JobGroup", back_populates="series")
    positions = relationship("JobPosition", back_populates="series")

class JobPosition(Base):
    __tablename__ = "job_positions"
    id = Column(String, primary_key=True, default=generate_uuid)
    series_id = Column(String, ForeignKey("job_series.id"))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    grade = Column(Enum(JobGrade), nullable=True)
    is_future_model = Column(Boolean, default=False)
    
    series = relationship("JobSeries", back_populates="positions")
    user = relationship("User", back_populates="job_positions")
    tasks = relationship("JobTask", back_populates="position")

class JobTask(Base):
    __tablename__ = "job_tasks"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    task_name = Column(String, nullable=False)
    action_verb = Column(String, nullable=True)
    task_object = Column(String, nullable=True)
    
    # AI Impact Analysis
    ai_substitution = Column(Float, default=0.0)
    ai_augmentation = Column(Float, default=0.0)
    ai_generation = Column(Float, default=0.0)
    
    position = relationship("JobPosition", back_populates="tasks")
    work_items = relationship("WorkItem", back_populates="task")

# --- Workload Analysis ---
class SurveyPeriod(Base):
    __tablename__ = "survey_periods"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(SurveyStatus), default=SurveyStatus.DRAFT)
    
    entries = relationship("WorkloadEntry", back_populates="survey_period")

class WorkItem(Base):
    __tablename__ = "work_items"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_task_id = Column(String, ForeignKey("job_tasks.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    frequency = Column(Enum(TaskFrequency), nullable=True)
    seasonal_details = Column(String, nullable=True)
    estimated_hours_per_occurrence = Column(Float, default=0.0)
    workload_amount = Column(Float, default=0.0)
    
    task = relationship("JobTask", back_populates="work_items")

class WorkloadEntry(Base):
    __tablename__ = "workload_entries"
    id = Column(String, primary_key=True, default=generate_uuid)
    survey_period_id = Column(String, ForeignKey("survey_periods.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"))
    task_id = Column(String, ForeignKey("job_tasks.id"))
    
    volume = Column(Float, default=0.0) # Frequency
    standard_time = Column(Float, default=0.0) # Hours
    fte = Column(Float, default=0.0) # Calculated
    
    survey_period = relationship("SurveyPeriod", back_populates="entries")
    user = relationship("User", backref="workload_entries")
    task = relationship("JobTask", backref="workload_entries")

# --- External Benchmark ---
class ExternalBenchmarkData(Base):
    __tablename__ = "external_benchmark_data"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"), nullable=True)
    institution_type = Column(String, nullable=True) # e.g. "Public Corp"
    headcount_range = Column(String, nullable=True) # e.g. "100-300"
    budget_range = Column(String, nullable=True) # e.g. "100B-300B"
    
    avg_hcroi = Column(Float, default=0.0) # Human Capital ROI
    avg_hcva = Column(Float, default=0.0) # Human Capital Value Added
    
    institution = relationship("Institution", back_populates="benchmark_data")

class TeamBudget(Base):
    __tablename__ = "team_budgets"
    id = Column(String, primary_key=True, default=generate_uuid)
    org_unit_id = Column(String, ForeignKey("org_units.id"))
    year = Column(Integer, nullable=False)
    amount = Column(Float, default=0.0)
    
    org_unit = relationship("OrgUnit", back_populates="team_budgets")

# --- Workflow & Process ---
class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    source_task_id = Column(String, ForeignKey("job_tasks.id"))
    target_task_id = Column(String, ForeignKey("job_tasks.id"))
    dependency_type = Column(Enum(DependencyType), default=DependencyType.SEQUENTIAL)
    description = Column(String, nullable=True)
    
    source_task = relationship("JobTask", foreign_keys=[source_task_id], backref="next_tasks")
    target_task = relationship("JobTask", foreign_keys=[target_task_id], backref="prev_tasks")

# --- Phase 3: Job Evaluation ---
class JobEvaluation(Base):
    __tablename__ = "job_evaluations"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    score_expertise = Column(Float, default=0.0)
    score_responsibility = Column(Float, default=0.0)
    score_complexity = Column(Float, default=0.0)
    total_score = Column(Float, default=0.0)
    grade = Column(Enum(JobGrade), nullable=True)
    
    position = relationship("JobPosition", backref="evaluation")

class JobEvaluationScore(Base):
    __tablename__ = "job_evaluation_scores"
    id = Column(String, primary_key=True, default=generate_uuid)
    evaluation_id = Column(String, ForeignKey("job_evaluations.id"))
    rater_type = Column(Enum(RaterType), nullable=False)
    rater_user_id = Column(String, ForeignKey("users.id"), nullable=True) # Null for external
    
    score_expertise = Column(Float, default=0.0)
    score_responsibility = Column(Float, default=0.0)
    score_complexity = Column(Float, default=0.0)
    raw_total = Column(Float, default=0.0)
    
    # Bias Prevention
    z_score = Column(Float, default=0.0) # Statistical Normalization
    final_score = Column(Float, default=0.0) # After weighting
    
    evaluation = relationship("JobEvaluation", backref="scores")

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    summary = Column(Text, nullable=True)
    qualification_requirements = Column(Text, nullable=True)
    kpi_indicators = Column(Text, nullable=True)
    version = Column(Integer, default=1)
    
    position = relationship("JobPosition", backref="descriptions")

# --- Phase 4: HR Management ---
class PerformanceReview(Base):
    __tablename__ = "performance_reviews"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    year = Column(Integer, nullable=False)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.DRAFT)
    review_date = Column(Date, nullable=True)
    
    score_common = Column(Float, default=0.0) # Common Competency
    score_leadership = Column(Float, default=0.0) # Leadership
    score_job = Column(Float, default=0.0) # Job Performance (Calculated from Goals)
    total_score = Column(Float, default=0.0)
    grade = Column(String, nullable=True) # S, A, B, C, D
    
    user = relationship("User", backref="reviews")
    goals = relationship("PerformanceGoal", back_populates="review")

class PerformanceGoal(Base):
    __tablename__ = "performance_goals"
    id = Column(String, primary_key=True, default=generate_uuid)
    review_id = Column(String, ForeignKey("performance_reviews.id"))
    category = Column(String, nullable=False) # e.g. "MBO", "BSC_FINANCIAL"
    goal_text = Column(Text, nullable=False)
    weight = Column(Float, default=0.0) # Percentage (0-100)
    target = Column(Text, nullable=True)
    actual = Column(Text, nullable=True)
    
    self_score = Column(Float, default=0.0)
    supervisor_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    
    review = relationship("PerformanceReview", back_populates="goals")

class PromotionList(Base):
    __tablename__ = "promotion_lists"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    target_grade = Column(Enum(JobGrade), nullable=False)
    rank = Column(Integer, nullable=False)
    total_points = Column(Float, default=0.0)
    
    user = relationship("User", backref="promotion_entries")

class TrainingProgram(Base):
    __tablename__ = "training_programs"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration_hours = Column(Float, default=0.0)
    target_job_series_id = Column(String, ForeignKey("job_series.id"), nullable=True)
    required_competency = Column(String, nullable=True)
    
    series = relationship("JobSeries", backref="training_programs")

class EmployeeTraining(Base):
    __tablename__ = "employee_trainings"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    program_id = Column(String, ForeignKey("training_programs.id"))
    status = Column(Enum(TrainingStatus), default=TrainingStatus.PLANNED)
    completion_date = Column(Date, nullable=True)
    score = Column(Float, nullable=True)
    
    user = relationship("User", backref="trainings")
    program = relationship("TrainingProgram", backref="attendees")

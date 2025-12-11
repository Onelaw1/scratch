from sqlalchemy.orm import Session
from . import models, schemas

# Institution CRUD
def get_institution(db: Session, institution_id: str):
    return db.query(models.Institution).filter(models.Institution.id == institution_id).first()

def get_institutions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Institution).offset(skip).limit(limit).all()

def create_institution(db: Session, institution: schemas.InstitutionCreate):
    db_institution = models.Institution(**institution.dict())
    db.add(db_institution)
    db.commit()
    db.refresh(db_institution)
    db.refresh(db_institution)
    return db_institution

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, institution_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.institution_id == institution_id).offset(skip).limit(limit).all()

# Job CRUD
# Job CRUD
# def get_jobs(db: Session, institution_id: str, skip: int = 0, limit: int = 100):
#     return db.query(models.Job).filter(models.Job.institution_id == institution_id).offset(skip).limit(limit).all()

# def create_job(db: Session, job: schemas.JobCreate, institution_id: str):
#     db_job = models.Job(**job.dict(), institution_id=institution_id)
#     db.add(db_job)
#     db.commit()
#     db.refresh(db_job)
#     return db_job

# Workload CRUD
def create_workload_entry(db: Session, entry: schemas.WorkloadEntryCreate):
    db_entry = models.WorkloadEntry(**entry.dict())
    
    # Principle 3: FTE Calculation
    # FTE = (Standard Time * Volume) / 1920 (Annual Standard Hours)
    if db_entry.standard_time and db_entry.volume:
        db_entry.fte_value = (db_entry.standard_time * db_entry.volume) / 1920.0
    else:
        db_entry.fte_value = 0.0

    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# Job Task CRUD
# Job Task CRUD
# def create_job_task(db: Session, task: schemas.JobTaskCreate, job_id: str):
#     # Principle 1: Granularity Control (Rule of 30)
#     current_count = db.query(models.JobTask).filter(models.JobTask.job_id == job_id).count()
#     if current_count >= 30:
#         raise ValueError("Job cannot have more than 30 tasks (Rule of 30).")

#     db_task = models.JobTask(**task.dict(), job_id=job_id)
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return db_task

# def get_job_tasks(db: Session, job_id: str):
#     return db.query(models.JobTask).filter(models.JobTask.job_id == job_id).all()

# Survey CRUD
def create_survey_period(db: Session, survey: schemas.SurveyPeriodCreate, institution_id: str):
    db_survey = models.SurveyPeriod(**survey.dict(), institution_id=institution_id)
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey

def get_survey_periods(db: Session, institution_id: str):
    return db.query(models.SurveyPeriod).filter(models.SurveyPeriod.institution_id == institution_id).all()

def get_workload_entries(db: Session, survey_period_id: str):
    return db.query(models.WorkloadEntry).filter(models.WorkloadEntry.survey_period_id == survey_period_id).all()

# Organizational Unit CRUD
def create_organizational_unit(db: Session, unit: schemas.OrganizationalUnitCreate):
    db_unit = models.OrganizationalUnit(**unit.dict())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

def get_organizational_units(db: Session, institution_id: str, parent_id: str = None):
    query = db.query(models.OrganizationalUnit).filter(models.OrganizationalUnit.institution_id == institution_id)
    if parent_id:
        query = query.filter(models.OrganizationalUnit.parent_id == parent_id)
    return query.all()

# Task Dependency CRUD
def create_task_dependency(db: Session, dependency: schemas.TaskDependencyCreate):
    db_dependency = models.TaskDependency(**dependency.dict())
    db.add(db_dependency)
    db.commit()
    db.refresh(db_dependency)
    return db_dependency

def get_task_dependencies(db: Session, task_id: str):
    return db.query(models.TaskDependency).filter(
        (models.TaskDependency.source_task_id == task_id) | 
        (models.TaskDependency.target_task_id == task_id)
    ).all()

# Job Improvement CRUD
def create_job_improvement(db: Session, improvement: schemas.JobImprovementCreate):
    db_improvement = models.JobImprovement(**improvement.dict())
    db.add(db_improvement)
    db.commit()
    db.refresh(db_improvement)
    return db_improvement

def get_job_improvements(db: Session, job_id: str):
    return db.query(models.JobImprovement).filter(models.JobImprovement.job_id == job_id).all()

# Time Validation
def validate_employee_annual_hours(db: Session, user_id: str, survey_period_id: str):
    """
    Validate that an employee's total annual hours are reasonable.
    Returns a dict with total_hours, expected_hours, and is_valid.
    """
    workload_entries = db.query(models.WorkloadEntry).filter(
        models.WorkloadEntry.user_id == user_id,
        models.WorkloadEntry.survey_period_id == survey_period_id
    ).all()
    
    total_hours = sum(entry.actual_hours_per_year for entry in workload_entries)
    
    # Standard work year: ~1,920 hours (40 hours/week * 48 weeks)
    expected_hours = 1920
    tolerance = 0.2  # 20% tolerance
    
    is_valid = (expected_hours * (1 - tolerance)) <= total_hours <= (expected_hours * (1 + tolerance))
    
    return {
        "total_hours": total_hours,
        "expected_hours": expected_hours,
        "is_valid": is_valid,
        "variance_percent": ((total_hours - expected_hours) / expected_hours) * 100
    }

# Strategic Analysis CRUD
def create_strategic_analysis(db: Session, analysis: schemas.StrategicAnalysisCreate):
    db_analysis = models.StrategicAnalysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def get_strategic_analyses(db: Session, institution_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.StrategicAnalysis).filter(models.StrategicAnalysis.institution_id == institution_id).offset(skip).limit(limit).all()

def get_strategic_analysis(db: Session, analysis_id: str):
    return db.query(models.StrategicAnalysis).filter(models.StrategicAnalysis.id == analysis_id).first()

def update_strategic_analysis(db: Session, analysis_id: str, analysis_update: schemas.StrategicAnalysisUpdate):
    db_analysis = db.query(models.StrategicAnalysis).filter(models.StrategicAnalysis.id == analysis_id).first()
    if db_analysis:
        update_data = analysis_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_analysis, key, value)
        db.commit()
        db.refresh(db_analysis)
    return db_analysis

def delete_strategic_analysis(db: Session, analysis_id: str):
    db_analysis = db.query(models.StrategicAnalysis).filter(models.StrategicAnalysis.id == analysis_id).first()
    if db_analysis:
        db.delete(db_analysis)
        db.commit()
    return db_analysis

# Job Analysis Enhancement CRUD (Principle 1)
def create_action_verb(db: Session, verb: schemas.ActionVerbCreate):
    db_verb = models.ActionVerb(**verb.dict())
    db.add(db_verb)
    db.commit()
    db.refresh(db_verb)
    return db_verb

def get_action_verbs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ActionVerb).offset(skip).limit(limit).all()

def create_task_dictionary_item(db: Session, item: schemas.TaskDictionaryCreate):
    db_item = models.TaskDictionary(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_task_dictionary_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TaskDictionary).offset(skip).limit(limit).all()

# Job Classification Enhancement CRUD (Principle 2)
def create_ncs_mapping(db: Session, mapping: schemas.NCSMappingCreate):
    db_mapping = models.NCSMapping(**mapping.dict())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

def get_ncs_mappings(db: Session, job_position_id: str):
    return db.query(models.NCSMapping).filter(models.NCSMapping.job_position_id == job_position_id).all()

# Job Evaluation Enhancement CRUD (Principle 6)
def create_point_table(db: Session, table: schemas.PointTableCreate):
    db_table = models.PointTable(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_point_table(db: Session, factor_id: str):
    return db.query(models.PointTable).filter(models.PointTable.factor_id == factor_id).all()

def create_job_evaluation_result(db: Session, result: schemas.JobEvaluationResultCreate):
    db_result = models.JobEvaluationResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_job_evaluation_result(db: Session, job_id: str):
    return db.query(models.JobEvaluationResult).filter(models.JobEvaluationResult.job_id == job_id).first()


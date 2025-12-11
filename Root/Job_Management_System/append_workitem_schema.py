
schema_code = """
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
"""

with open("c:/Users/Administrator/Downloads/Root/Job_Management_System/backend/schemas.py", "a") as f:
    f.write(schema_code)
print("WorkItem schemas appended successfully.")

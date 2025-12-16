
schema_code = """
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
"""

with open("c:/Users/Administrator/Downloads/Root/Job_Management_System/backend/schemas.py", "a") as f:
    f.write(schema_code)
print("Schema appended successfully.")

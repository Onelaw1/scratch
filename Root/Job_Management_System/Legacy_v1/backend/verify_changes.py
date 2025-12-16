import sys
import os

# Add the current working directory to sys.path
sys.path.append(os.getcwd())

try:
    from backend.models import TaskFrequency, JobTask
    from backend.schemas import JobTaskBase
    import enum

    print("Checking TaskFrequency enum...")
    if "YEARLY" in TaskFrequency.__members__ and "SEASONAL" in TaskFrequency.__members__:
        print("PASS: TaskFrequency has YEARLY and SEASONAL.")
    else:
        print("FAIL: TaskFrequency missing YEARLY or SEASONAL.")

    print("Checking JobTask model...")
    if hasattr(JobTask, "seasonal_details"):
        print("PASS: JobTask has seasonal_details.")
    else:
        print("FAIL: JobTask missing seasonal_details.")

    print("Checking JobTaskBase schema...")
    if "seasonal_details" in JobTaskBase.model_fields:
        print("PASS: JobTaskBase has seasonal_details.")
    else:
        print("FAIL: JobTaskBase missing seasonal_details.")

except Exception as e:
    print(f"FAIL: Exception occurred: {e}")
    import traceback
    traceback.print_exc()

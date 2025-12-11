import sys
import os

# Path to Job Management System backend
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Job_Management_System', 'backend'))
print(f"Backend Path: {backend_path}")

if os.path.exists(backend_path):
    print("Backend path exists.")
else:
    print("Backend path DOES NOT exist.")

sys.path.append(backend_path)
print(f"Sys Path: {sys.path}")

try:
    import models
    print("Successfully imported models.")
    print(dir(models))
except ImportError as e:
    print(f"Failed to import models: {e}")
except Exception as e:
    print(f"An error occurred during import: {e}")

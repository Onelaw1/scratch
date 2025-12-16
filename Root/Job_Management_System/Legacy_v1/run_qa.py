
import sys
import os
import pytest

# Add the current directory (Root/Job_Management_System) to sys.path
# This ensures that 'backend' package can be imported from anywhere
sys.path.append(os.getcwd())

if __name__ == "__main__":
    print(f"Running QA from {os.getcwd()}")
    # Run pytest on the backend/tests folder
    exit_code = pytest.main(["backend/tests"])
    sys.exit(exit_code)

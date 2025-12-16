
import sys
import os

print(f"CWD: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    import backend
    print("Imported backend package")
except ImportError as e:
    print(f"Failed to import backend: {e}")

try:
    from backend.main import app
    print("Imported app from backend.main")
except ImportError as e:
    print(f"Failed to import backend.main: {e}")

try:
    from backend.tests import conftest
    print("Imported conftest")
except ImportError as e:
    print(f"Failed to import conftest: {e}")

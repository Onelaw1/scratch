import sys
import os
from fastapi.testclient import TestClient

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

try:
    from backend.main import app
    client = TestClient(app)
    response = client.get("/health")
    if response.status_code == 200:
        print("✅ Backend Startup Successful")
    else:
        print(f"❌ Backend Startup Failed: {response.status_code}")
except Exception as e:
    print(f"❌ Backend Startup Error: {e}")
    import traceback
    traceback.print_exc()

import requests
import sys

def verify_endpoints():
    base_url = "http://localhost:8000"
    endpoints = [
        "/web/job-description-editor",
        "/web/job-evaluation",
        "/web/job-classification",
        "/web/workload-survey"
    ]
    
    print("Verifying UI Endpoints...")
    all_passed = True
    
    for endpoint in endpoints:
        try:
            # We can't easily test full HTML rendering without a running server, 
            # but we can check if the router is set up correctly by importing the app.
            # However, importing app might trigger DB connections.
            # Let's just assume the user will run the server.
            # For this script, I'll just print what to test manually if server isn't running.
            
            # Actually, I can use TestClient from starlette/fastapi
            from fastapi.testclient import TestClient
            from backend.main import app
            
            client = TestClient(app)
            response = client.get(endpoint)
            
            if response.status_code == 200:
                print(f"[PASS] {endpoint}")
            else:
                print(f"[FAIL] {endpoint} returned {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"[ERROR] Could not test {endpoint}: {e}")
            all_passed = False
            
    if all_passed:
        print("\nAll UI endpoints verified successfully!")
    else:
        print("\nSome endpoints failed verification.")

if __name__ == "__main__":
    # Add root to path
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
    verify_endpoints()

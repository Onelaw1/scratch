import requests
import sys

# Base URL - adjust if server port differs
BASE_URL = "http://localhost:8000"

def test_endpoint(path, method="GET", expect_status=401):
    url = f"{BASE_URL}{path}"
    print(f"Testing {method} {url} without token...")
    try:
        if method == "GET":
            resp = requests.get(url)
        elif method == "POST":
            resp = requests.post(url, json={})
        
        if resp.status_code == expect_status:
            print(f"PASS: Got {resp.status_code} as expected.")
        else:
            print(f"FAIL: Got {resp.status_code}, expected {expect_status}.")
    except Exception as e:
        print(f"ERROR: Could not connect to {url}. Is the server running? ({e})")

if __name__ == "__main__":
    print("--- Verifying RBAC Enforcement (No Token) ---")
    test_endpoint("/users/") 
    test_endpoint("/scenarios/", "POST")
    test_endpoint("/organization/groups", "POST")
    test_endpoint("/scientific/calibration/sessions") # Example of deeper path
    print("--- Verification Complete ---")

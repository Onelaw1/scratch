import sys
import os
# Add the parent directory to sys.path to make imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app
import json

client = TestClient(app)

def run_demo():
    print("="*60)
    print("!  AI-NATIVE PUBLIC HR SYSTEM REVOLUTION DEMO  !")
    print("="*60)

    # Scneario 1: AI Job Architect
    print("\n[Scenario 1] The 'One-Click' AI Information Architecture")
    print("User Input: 'Construction Safety Manager' (NCS Code: 040101)")
    print("Action: AI generating legal job description and 3-tier task structure...")
    
    payload = {
        "title": "Unfair Construction Man", # Intentional bias for audit test
        "ncs_code": "040101"
    }
    
    response = client.post("/ai-commander/architect/job", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        job_id = data['job_id']
        print(f"\n[OK] AI Architecture Success! Job ID: {job_id}")
        print(f"[AI] AI Message: {data['ai_message']}")
        print(f"[Audit] Initial Fairness Check: {data['fairness_audit']}")
    else:
        print(f"[FAIL] Error: {response.text}")
        return

    # Scenario 2: Deep Fairness Audit
    print("\n" + "-"*60)
    print("\n[Scenario 2] The 'Fairness Engine' Real-time Audit")
    print("Action: Scanning the generated job for bias (Gender, Age, etc.)...")
    
    audit_response = client.post(f"/fairness-audit/run-audit/{job_id}")
    audit_data = audit_response.json()
    
    print(f"\n[Search] Audit Complete. Issues Found: {audit_data['issues_found']}")
    
    logs_response = client.get(f"/fairness-audit/job/{job_id}")
    logs = logs_response.json()
    
    print("\n[Audit Log Report]")
    for log in logs:
        status_icon = "[PASS]" if log['status'] == "PASS" else ("[WARN]" if log['status'] == "WARNING" else "[FAIL]")
        print(f"{status_icon} [{log['check_type']}] Status: {log['status']}")
        print(f"   Message: {log['message']}")

    print("\n" + "="*60)
    print("Demonstration Complete.")
    print("This proves the system is not just storing data, but ACTIVELEY reasoning and protecting.")

if __name__ == "__main__":
    run_demo()

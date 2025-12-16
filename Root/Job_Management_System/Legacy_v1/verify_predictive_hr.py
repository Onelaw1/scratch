import requests
import uuid

BASE_URL = "http://localhost:8000"

def verify_predictive_hr():
    try:
        print("1. Testing Turnover Model Training...")
        # Since logic is mocked, this should return success immediately
        resp = requests.post(f"{BASE_URL}/scientific/prediction/turnover/train")
        if resp.status_code != 200:
            print(f"Train Failed: {resp.text}")
        else:
            print(f"Train Success: {resp.json()}")

        # 2. Testing Prediction (Need a User ID)
        # Fetch users first
        users_resp = requests.get(f"{BASE_URL}/users")
        users = users_resp.json()
        if not users:
            print("No users found to test prediction.")
            return

        test_user = users[0]['id']
        print(f"Testing Prediction for User ID: {test_user}")
        
        pred_resp = requests.get(f"{BASE_URL}/scientific/prediction/turnover/{test_user}")
        print(f"Prediction: {pred_resp.json()}")
        assert 'risk_score' in pred_resp.json()
        
        print("3. Testing Career Recommendation...")
        career_resp = requests.get(f"{BASE_URL}/scientific/prediction/career/{test_user}")
        print(f"Recommendations: {career_resp.json()}")
        assert isinstance(career_resp.json(), list)
        
        print(">>> PREDICTIVE HR VERIFICATION SUCCESSFUL! <<<")
        
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")

if __name__ == "__main__":
    verify_predictive_hr()

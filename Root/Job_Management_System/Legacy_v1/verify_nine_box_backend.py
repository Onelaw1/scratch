
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import Base, get_db
from backend.services.nine_box_service import NineBoxService
from backend import models

# Setup Test DB connection (using the actual dev db for verification as per user context)
# In real prod, we would use a test db, but here we want to verify against the current state
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_verification():
    print("=== 9-Box Grid Service Verification (Direct) ===\n")
    
    db = TestingSessionLocal()
    service = NineBoxService(db)
    
    try:
        # 0. Seed Mock Data if Empty
        print("[0] Checking Data...")
        users = db.query(models.User).all()
        target_user = None
        
        if not users:
            print(" -> No users found. Creating mock user...")
            target_user = models.User(id="user_9box_test", name="NineBox Tester", email="test@example.com")
            db.add(target_user)
            db.commit()
        else:
            target_user = users[0]
            
        # Check for review
        review = db.query(models.PerformanceReview).filter(models.PerformanceReview.user_id == target_user.id).first()
        if not review:
             print(f" -> Creating mock review for {target_user.name}...")
             review = models.PerformanceReview(
                id=f"review_{target_user.id}_2024",
                user_id=target_user.id,
                year=2024,
                status=models.ReviewStatus.FINAL, # Must be FINAL
                total_score=85.0, 
                score_potential=85.0
            )
             db.add(review)
             db.commit()
             print(" -> Seeded Review (85/85)")
        
        # 1. Auto Map
        print("[1] Running Auto-Map...")
        res = service.auto_map_all()
        print(f"[SUCCESS] Auto-Map Success: Updated {res['updated_count']} records")
        
        # 2. Fetch Grid
        print("\n[2] Fetching Grid Data...")
        data = service.get_grid_data()
        total = data.get("total_employees", 0)
        print(f"[SUCCESS] Fetched {total} employees")
        
        if total == 0:
            print("[WARNING] No employees found. Skipping move test.")
            return

        # 3. Test Manual Move
        target_employee = data['employees'][0]
        review_id = target_employee.get("review_id")
        current_box = target_employee.get("box")
        user_name = target_employee.get("name")
        
        target_box = 9 if current_box != 9 else 1
        
        print(f"\n[3] Testing Move for {user_name} ({current_box} -> {target_box})...")
        
        result = service.update_box_position(review_id, target_box)
        
        if result['box'] == target_box:
           print(f"[SUCCESS] Move Success: Employee is now in Box {result['box']} ({result['category']})")
        else:
           print(f"[FAIL] Move Failed: {result}")
           
        # 4. Verify Persistence
        print("\n[4] Verifying Persistence...")
        # Re-fetch
        data = service.get_grid_data()
        updated_emp = next((e for e in data['employees'] if e['review_id'] == review_id), None)
        
        if updated_emp and updated_emp['box'] == target_box:
            print("[SUCCESS] Persistence Verified")
        else:
            print(f"[FAIL] Persistence Failed: Got {updated_emp['box'] if updated_emp else 'None'}")
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_verification()

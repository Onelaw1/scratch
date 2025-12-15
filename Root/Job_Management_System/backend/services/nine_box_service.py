from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models

class NineBoxService:
    def __init__(self, db: Session):
        self.db = db

    def generate_grid_data(self) -> Dict[str, Any]:
        """
        Generates 9-Box Grid Data for all employees based on their latest Performance Review.
        Mapping:
        X-Axis: Performance (total_score) -> 0-100
        Y-Axis: Potential (score_potential) -> 0-100
        """
        
        # 1. Fetch all users with their latest finalized relevant reviews
        # optimization: Fetch Users joined with PerformanceReview
        # For simplicity, we fetch all users and their latest review
        
        users = self.db.query(models.User).all()
        grid_data = []

        for user in users:
            # Get latest finalized review
            review = self.db.query(models.PerformanceReview)\
                .filter(models.PerformanceReview.user_id == user.id)\
                .filter(models.PerformanceReview.status == models.ReviewStatus.FINAL)\
                .order_by(models.PerformanceReview.year.desc())\
                .first()
            
            if not review:
                continue

            perf_score = review.total_score
            pot_score = review.score_potential
            
            box, category, color = self._calculate_box_position(perf_score, pot_score)
            
            # Update review with calculated box if not already set (or always update to sync)
            if review.nine_box_position != box:
                review.nine_box_position = box
                self.db.add(review) # Mark for update

            grid_data.append({
                "id": user.id,
                "name": user.name,
                "dept": user.org_unit.name if user.org_unit else "N/A",
                "performance": perf_score,
                "potential": pot_score,
                "box": box,
                "category": category,
                "color": color
            })
            
        self.db.commit() # Commit any box updates

        return {
            "generated_at": datetime.now().strftime("%Y-%m-%d"),
            "total_employees": len(grid_data),
            "distribution": {
                "Star": len([e for e in grid_data if e["box"] == 9]),
                "Core": len([e for e in grid_data if e["box"] == 5]),
                "Risk": len([e for e in grid_data if e["box"] == 1]),
            },
            "employees": grid_data
        }

    def _calculate_box_position(self, perf_score: float, pot_score: float):
        """
        Calculates 1-9 Box position.
        Performance (X): High(>=90), Mod(>=70), Low(<70) -> Adjusted for strictness
        Let's use standard: High(>=80), Mod(>=60), Low(<60) for demo
        Potential (Y): High(>=80), Mod(>=60), Low(<60)
        """
        
        # Thresholds
        HIGH_CUTOFF = 80
        MOD_CUTOFF = 60
        
        box = 0
        category = ""
        color = ""

        if pot_score >= HIGH_CUTOFF: # High Potential (Row 3)
            if perf_score >= HIGH_CUTOFF: box = 9; category = "Star"; color = "blue"
            elif perf_score >= MOD_CUTOFF: box = 8; category = "High Potential"; color = "cyan"
            else: box = 7; category = "Enigma"; color = "yellow"
        elif pot_score >= MOD_CUTOFF: # Mod Potential (Row 2)
            if perf_score >= HIGH_CUTOFF: box = 6; category = "High Performer"; color = "green"
            elif perf_score >= MOD_CUTOFF: box = 5; category = "Core Player"; color = "gray"
            else: box = 4; category = "Inconsistent"; color = "orange"
        else: # Low Potential (Row 1)
            if perf_score >= HIGH_CUTOFF: box = 3; category = "Trusted Pro"; color = "teal"
            elif perf_score >= MOD_CUTOFF: box = 2; category = "Effective"; color = "gray"
            else: box = 1; category = "Risk / Exit"; color = "red"
            
        return box, category, color

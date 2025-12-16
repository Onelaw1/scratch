from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models

class NineBoxService:
    def __init__(self, db: Session):
        self.db = db

    def get_grid_data(self) -> Dict[str, Any]:
        """
        Fetches 9-Box Grid Data from the database.
        """
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

            # If box is not set, calculate it on the fly but don't save unless auto-map is called
            box = review.nine_box_position
            category = ""
            color = ""
            
            if not box:
                 box, category, color = self._calculate_box_position(review.total_score, review.score_potential)
            else:
                 # Get styling for existing box
                 _, category, color = self._get_box_metadata(box)

            grid_data.append({
                "id": user.id,
                "review_id": review.id,
                "name": user.name,
                "dept": user.org_unit.name if user.org_unit else "N/A",
                "performance": review.total_score,
                "potential": review.score_potential,
                "box": box,
                "category": category,
                "color": color
            })
            
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

    def auto_map_all(self):
        """
        Force resets all employees' 9-box position based on their scores.
        """
        users = self.db.query(models.User).all()
        count = 0
        for user in users:
            review = self.db.query(models.PerformanceReview)\
                .filter(models.PerformanceReview.user_id == user.id)\
                .filter(models.PerformanceReview.status == models.ReviewStatus.FINAL)\
                .order_by(models.PerformanceReview.year.desc())\
                .first()
            
            if review:
                box, _, _ = self._calculate_box_position(review.total_score, review.score_potential)
                review.nine_box_position = box
                self.db.add(review)
                count += 1
        
        self.db.commit()
        return {"updated_count": count}

    def update_box_position(self, review_id: str, new_box: int):
        """
        Manually moves an employee to a different box (Calibration).
        """
        review = self.db.query(models.PerformanceReview).filter(models.PerformanceReview.id == review_id).first()
        if not review:
            raise ValueError("Review not found")
            
        review.nine_box_position = int(new_box)
        self.db.commit()
        
        _, category, color = self._get_box_metadata(new_box)
        return {"id": review.id, "box": new_box, "category": category, "color": color}

    def _get_box_metadata(self, box: int):
        # Helper to get name/color for a box ID
        meta = {
            9: ("Star Superformer", "blue"),
            8: ("High Potential", "cyan"),
            7: ("Enigma (High Pot)", "yellow"),
            6: ("High Performer", "green"),
            5: ("Core Player", "gray"),
            4: ("Inconsistent", "orange"),
            3: ("Trusted Professional", "teal"),
            2: ("Effective", "gray"),
            1: ("Risk / Underperformer", "red")
        }
        name, color = meta.get(box, ("Unknown", "gray"))
        return box, name, color

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

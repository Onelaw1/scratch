from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import User, JobGrade

class WageSimulationService:
    """
    Core engine for 'Seniority -> Job-Based' Wage Transition.
    """

    def calculate_pay_bands(self, 
                            min_base: float = 30000000, 
                            max_cap: float = 100000000, 
                            grades: List[str] = ["G1", "G2", "G3", "G4", "G5"],
                            spread: float = 0.3) -> Dict[str, Dict[str, float]]:
        """
        Generates Pay Bands for each grade.
        Simple logic: Linear progression of Mid-points, with defined Spread.
        Spread = (Max - Min) / Min
        """
        bands = {}
        step = (max_cap - min_base) / (len(grades) - 1)
        
        current_mid = min_base
        for i, grade in enumerate(grades):
            # Calculate Min/Max based on Spread around Mid
            # If Spread is 30% (0.3), Range = Min * 1.3 = Max
            # Mid is typically (Min + Max) / 2
            # Let's verify: Mid = Min * (1 + Spread/2)? No.
            # Standard Formula: Min = Mid / (1 + Spread/2), Max = Min * (1 + Spread)
            
            # Simplified for Demo: 
            # Min = Mid * (1 - Spread/2)
            # Max = Mid * (1 + Spread/2)
            
            band_min = current_mid * (1 - spread/3) 
            band_max = current_mid * (1 + spread/3)
            
            bands[grade] = {
                "min": round(band_min, -4), # Round to nearest 10,000 KRW
                "mid": round(current_mid, -4),
                "max": round(band_max, -4)
            }
            current_mid += step
            
        return bands

    def run_simulation(self, db: Session, spread: float, base_increase_pct: float) -> Dict[str, Any]:
        """
        Simulates the cost impact.
        - spread: Pay Band width (0.2 ~ 0.5)
        - base_increase_pct: Across-the-board increase (e.g. 0.02 for 2%)
        """
        users = db.query(User).all()
        # Mock assigning grades if missing (Random distribution for demo)
        # In real app, use User -> JobPosition -> JobGrade
        
        bands = self.calculate_pay_bands(spread=spread)
        
        total_current_cost = 0
        total_new_cost = 0
        impacted_below = 0
        impacted_above = 0
        user_results = []
        
        # Mock Grade Mapping for users without grades
        mock_grades = ["G1", "G2", "G3", "G4", "G5"]
        
        for i, user in enumerate(users):
            current_pay = user.current_salary if user.current_salary else 50000000
            
            # Assign fake grade if needed for simulation
            # Heuristic: salary based grade estimation
            if current_pay < 40000000: grade = "G1"
            elif current_pay < 60000000: grade = "G2"
            elif current_pay < 80000000: grade = "G3"
            elif current_pay < 100000000: grade = "G4"
            else: grade = "G5"
            
            band = bands[grade]
            
            # Logic:
            # 1. Apply Base Increase first
            step1_pay = current_pay * (1 + base_increase_pct)
            
            # 2. Check Band Compliance
            final_pay = step1_pay
            adjustment = 0
            status = "IN_BAND"
            
            if step1_pay < band["min"]:
                final_pay = band["min"] # Bring up to Min
                adjustment = final_pay - step1_pay
                status = "BELOW_MIN"
                impacted_below += 1
            elif step1_pay > band["max"]:
                # Usually Red Circle (Freeze), but cost is simply the Step1 Pay
                final_pay = step1_pay 
                status = "ABOVE_MAX"
                impacted_above += 1
            
            total_current_cost += current_pay
            total_new_cost += final_pay
            
            user_results.append({
                "name": user.name,
                "grade": grade,
                "current_salary": current_pay,
                "new_salary": final_pay,
                "band_min": band["min"],
                "band_max": band["max"],
                "status": status
            })
            
        return {
            "summary": {
                "total_current_cost": total_current_cost,
                "total_new_cost": total_new_cost,
                "increase_amount": total_new_cost - total_current_cost,
                "increase_pct": ((total_new_cost - total_current_cost) / total_current_cost * 100) if total_current_cost > 0 else 0,
                "impacted_below_count": impacted_below,
                "impacted_above_count": impacted_above
            },
            "bands": bands,
            "scatter_data": user_results
        }

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
import random
import statistics
from datetime import datetime
from ..models import User

class PromotionService:
    """
    Scientific Promotion Analysis.
    Compares "Tenure-based" vs "Slope-based" (Growth Rate) strategies.
    """

    def _calculate_slope(self, scores: List[float]) -> float:
        """
        Calculates Linear Regression Slope (Growth Rate).
        """
        if len(scores) < 2: return 0.0
        n = len(scores)
        if n == 0: return 0.0
        
        # X axis = time [0, 1, 2...]
        xs = list(range(n))
        ys = scores
        
        mean_x = statistics.mean(xs)
        mean_y = statistics.mean(ys)
        
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        denominator = sum((x - mean_x) ** 2 for x in xs)
        
        if denominator == 0: return 0.0
        return numerator / denominator

    def simulate_promotion(self, db: Session) -> Dict[str, Any]:
        users = db.query(User).all()
        candidates = []
        
        # 1. Generate Data & Calculate Metrics
        for user in users:
            # Mock Tenure (Years)
            tenure = random.randint(1, 10)
            
            # Mock 3-Year Performance History
            # Randomize trajectory based on mock tenure/persona to make it interesting
            base_score = 3.0 + (random.random() * 1.5)
            history = []
            
            # Create different growth patterns
            pattern = random.choice(["FLAT", "GROWTH", "DECLINE", "ROCKET"])
            
            for i in range(3):
                noise = random.uniform(-0.2, 0.2)
                if pattern == "FLAT": score = base_score + noise
                elif pattern == "GROWTH": score = base_score + (i * 0.3) + noise
                elif pattern == "DECLINE": score = base_score - (i * 0.2) + noise
                elif pattern == "ROCKET": score = base_score + (i * 0.6) + noise
                else: score = base_score
                
                # Cap
                score = min(max(score, 1.0), 5.0)
                history.append(score)
            
            slope = self._calculate_slope(history)
            current_score = history[-1]
            
            candidates.append({
                "user_id": user.id,
                "name": user.name,
                "position": user.position.title if user.position else "Employee",
                "tenure": tenure,
                "history": history,
                "current_score": round(current_score, 2),
                "growth_slope": round(slope, 3)
            })
            
        # 2. Scenario A: Traditional (Tenure-based)
        # Select top 5 by Tenure, tie-break by Current Score
        scenario_a = sorted(candidates, key=lambda x: (x["tenure"], x["current_score"]), reverse=True)[:5]
        
        # 3. Scenario B: Scientific (Slope-based)
        # Select top 5 by Growth Slope, tie-break by Current Score
        scenario_b = sorted(candidates, key=lambda x: (x["growth_slope"], x["current_score"]), reverse=True)[:5]
        
        # 4. Compare Talent Density (Avg Slope of selected candidates)
        density_a = statistics.mean([c["growth_slope"] for c in scenario_a])
        density_b = statistics.mean([c["growth_slope"] for c in scenario_b])
        
        # Identify "Hidden Gems" (In B but not in A)
        ids_a = set(c["user_id"] for c in scenario_a)
        hidden_gems = [c for c in scenario_b if c["user_id"] not in ids_a]
        
        return {
            "total_candidates": len(candidates),
            "scenario_a": {
                "strategy": "Traditional (Tenure)",
                "avg_growth_slope": round(density_a, 3),
                "candidates": scenario_a
            },
            "scenario_b": {
                "strategy": "Scientific (Growth Slope)",
                "avg_growth_slope": round(density_b, 3),
                "candidates": scenario_b
            },
            "hidden_gems": hidden_gems
        }

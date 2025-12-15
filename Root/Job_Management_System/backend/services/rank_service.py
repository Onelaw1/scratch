import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..models import User, JobPosition

class RankService:
    def __init__(self, db_session):
        self.db = db_session

    def generate_rank_list(self) -> Dict[str, Any]:
        """
        Generates a binding "Scientific Promotion Rank List".
        Calculates SPS for eligible candidates and sorts them.
        """
        # 1. Fetch Candidates (Simulated for Demo)
        candidates = self._fetch_eligible_candidates()

        # 2. Calculate SPS for each
        ranked_list = []
        for cand in candidates:
            sps_data = self._calculate_sps(cand)
            cand.update(sps_data)
            ranked_list.append(cand)

        # 3. Sort by Total Score Descending
        ranked_list.sort(key=lambda x: x["total_score"], reverse=True)

        # 4. Assign Tiers
        total_count = len(ranked_list)
        for i, item in enumerate(ranked_list):
            percentile = (i + 1) / total_count
            if percentile <= 0.1:
                item["tier"] = "Certain (확정)"
                item["tier_color"] = "teal"
            elif percentile <= 0.3:
                item["tier"] = "Probable (유력)"
                item["tier_color"] = "blue"
            else:
                item["tier"] = "Hold (보류)"
                item["tier_color"] = "gray"
            
            item["rank"] = i + 1

        return {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_candidates": total_count,
            "rank_list": ranked_list
        }

    def _fetch_eligible_candidates(self) -> List[Dict[str, Any]]:
        # Simulate ~20 candidates with diverse profiles
        names = [
            "Kim Chul-soo", "Lee Young-hee", "Park Ji-sung", "Choi Min-ho", "Jung Soo-jin",
            "Kang Ha-neul", "Yoon Mirae", "Lim Jae-beom", "Song Hye-kyo", "Hyun Bin",
            "Son Heung-min", "Kim Yuna", "Bong Joon-ho", "Lee Jay", "Park Seo-joon",
            "IU", "PSY", "V", "Jimin", "Suga"
        ]
        
        candidates = []
        for i, name in enumerate(names):
            # Simulate realistic data Mix
            # Tenure: 2 ~ 10 years
            tenure = round(random.uniform(2.0, 10.0), 1)
            
            # Integral: 50 ~ 100 (History of performance)
            integral = round(random.uniform(50.0, 100.0), 1)
            
            # Slope: -0.5 ~ +2.0 (Growth rate)
            # Make sure we have some "Hidden Gems" (Low Tenure, High Slope)
            if tenure < 4.0 and random.random() > 0.7:
                slope = round(random.uniform(1.2, 2.0), 2) # High potential
            else:
                slope = round(random.uniform(-0.2, 1.2), 2)

            candidates.append({
                "user_id": 100 + i,
                "name": name,
                "department": random.choice(["Sales", "Engineering", "HR", "Finance", "Marketing"]),
                "current_grade": f"G{random.randint(3, 5)}",
                "tenure_years": tenure,
                "integral_score": integral,
                "growth_slope": slope
            })
        return candidates

    def _calculate_sps(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates Scientific Promotion Score (SPS).
        Formula: (Tenure * 10) + (Integral * 0.5) + (Slope * 30)
        *Calibrated to make max score approx 100-150 range.
        """
        w_tenure = 5.0  # Reduced weight for tenure
        w_integral = 0.6 # Integral is large (e.g. 80), so 0.6 => 48
        w_slope = 30.0  # Slope is small (e.g. 1.5), so 30 => 45 (High impact)

        s_tenure = candidate["tenure_years"] * w_tenure
        s_integral = candidate["integral_score"] * w_integral
        s_slope = candidate["growth_slope"] * w_slope

        total_score = s_tenure + s_integral + s_slope

        return {
            "score_tenure": round(s_tenure, 1),
            "score_integral": round(s_integral, 1),
            "score_slope": round(s_slope, 1),
            "total_score": round(total_score, 1)
        }

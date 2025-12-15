from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models

class SpanService:
    def __init__(self, db: Session):
        self.db = db

    def analyze_org_structure(self) -> Dict[str, Any]:
        """
        Analyzes Organization Structure for Span of Control and Layers.
        Uses User.reports_to relationship to build the tree.
        """
        
        # 1. Fetch all users
        users = self.db.query(models.User).all()
        
        # 2. Build Tree & Calculate Metrics
        # Find roots (those with no reports_to_id)
        roots = [u for u in users if u.reports_to_id is None]
        
        analysis_data = []
        alerts = []
        
        # Recursive traversal
        for root in roots:
            self._traverse_node(root, 0, analysis_data, alerts)
            
        # If no roots (circular or empty), fallback
        if not roots and users:
            # Taking one arbitrary user or handling error. For now, assume at least one root.
            pass

        # Metrics
        total_managers = len([d for d in analysis_data if d["span"] > 0])
        average_span = sum(d["span"] for d in analysis_data if d["span"] > 0) / total_managers if total_managers > 0 else 0
        max_depth = max((d["depth"] for d in analysis_data), default=0)

        return {
            "analyzed_at": datetime.now().strftime("%Y-%m-%d"),
            "metrics": {
                "average_span": round(average_span, 1),
                "max_layers": max_depth + 1,
                "total_managers": total_managers
            },
            "nodes": analysis_data,
            "alerts": alerts
        }

    def _traverse_node(self, user: models.User, depth: int, data_list: List[Dict], alerts: List[Dict]):
        # Calculate Span (Direct Reports)
        reports = user.direct_reports # managed by backref
        span = len(reports)
        
        # Determine Status
        status = "Individual Contributor"
        if span > 0:
            if span > 15: status = "Wide (Bottleneck)"
            elif span < 3: status = "Narrow (micro-mgmt)"
            else: status = "Optimal"
            
        # Role inference (simplistic)
        role = "Staff"
        if depth == 0: role = "Executive"
        elif span > 0: role = "Manager"
        
        node_data = {
            "id": user.id,
            "name": user.name,
            "role": role, 
            "span": span,
            "depth": depth,
            "status": status
        }
        data_list.append(node_data)
        
        # Generate Alerts
        if span > 15:
            alerts.append({"name": user.name, "issue": f"Bottleneck (Span: {span})", "severity": "High"})
        elif span < 3 and span > 0:
             alerts.append({"name": user.name, "issue": f"Micro-management (Span: {span})", "severity": "Medium"})

        # Recurse
        for report in reports:
            self._traverse_node(report, depth + 1, data_list, alerts)

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from .. import models

class SpanOfControlService:
    def __init__(self, db: Session):
        self.db = db

    def get_span_of_control_analysis(self) -> List[Dict[str, Any]]:
        """
        Builds the complete organizational hierarchy based on reporting lines (User.reports_to_id).
        Returns a list of root nodes (typically the CEO or top-level execs), each containing their full subtree.
        """
        users = self.db.query(models.User).all()
        
        # 1. Index users by ID for quick lookup and by reports_to_id for children finding
        user_map = {u.id: u for u in users}
        children_map: Dict[str, List[models.User]] = {}
        
        for u in users:
            if u.reports_to_id:
                if u.reports_to_id not in children_map:
                    children_map[u.reports_to_id] = []
                children_map[u.reports_to_id].append(u)
        
        # 2. Identify Root Nodes (No reports_to_id or reports_to_id pointing to non-existent user)
        roots = [u for u in users if not u.reports_to_id or u.reports_to_id not in user_map]
        
        # 3. Recursive Build
        result_tree = []
        for root in roots:
            node = self._build_node(root, children_map, 0)
            result_tree.append(node)
            
        return result_tree

    def _build_node(self, user: models.User, children_map: Dict[str, List[models.User]], depth: int) -> Dict[str, Any]:
        direct_reports = children_map.get(user.id, [])
        
        children_nodes = []
        total_descendants = 0
        
        for child in direct_reports:
            child_node = self._build_node(child, children_map, depth + 1)
            children_nodes.append(child_node)
            total_descendants += 1 + child_node['total_descendants']
            
        span_status = "OPTIMAL"
        if len(direct_reports) == 0:
            span_status = "LEAF" # Individual Contributor
        elif len(direct_reports) < 3:
            span_status = "NARROW"
        elif len(direct_reports) > 15:
            span_status = "WIDE"
            
        return {
            "id": user.id,
            "name": user.name,
            "title": user.job_positions[0].title if user.job_positions else "N/A",
            "org_unit": user.org_unit.name if user.org_unit else "N/A",
            "depth": depth,
            "span_count": len(direct_reports),
            "total_descendants": total_descendants,
            "span_status": span_status, 
            "children": children_nodes
        }

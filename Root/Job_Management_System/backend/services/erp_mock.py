from typing import List, Dict

class ERPMockService:
    """
    Simulates an external ERP System (e.g., SAP, Oracle).
    Provides access to "Official" Budget and Headcount data.
    """
    
    def fetch_org_structure_data(self) -> List[Dict]:
        """
        Simulates: GET /api/v1/org-structure from ERP
        Returns a list of dicts with keys: dept_code, dept_name, budget_millions, authorized_count
        """
        # Mock Data matches some existing departments but introduces differences
        return [
            {
                "dept_code": "STRAT-001", 
                "dept_name": "Strategic Planning Team", 
                "budget_millions": 1200, 
                "authorized_to": 8  # System might have 6
            },
            {
                "dept_code": "HR-002", 
                "dept_name": "Human Resources Team", 
                "budget_millions": 800, 
                "authorized_to": 12 # System might have 10
            },
            {
                "dept_code": "TECH-003", 
                "dept_name": "IT Development Team", 
                "budget_millions": 3500, 
                "authorized_to": 25
            },
            {
                "dept_code": "FIN-004", 
                "dept_name": "Finance & Audit Team", 
                "budget_millions": 900, 
                "authorized_to": 10
            }
        ]

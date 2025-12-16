from enum import Enum

class Role(str, Enum):
    SME = "SME"
    HR_MANAGER = "HR_Manager"
    TEAM_LEAD = "Team_Lead"
    EMPLOYEE = "Employee"
    MIDDLE_MANAGER = "Middle_Manager"
    ADMINISTRATOR = "Administrator"
    INSTITUTION_HEAD = "Institution_Head"
    EVALUATION_COMMITTEE = "Evaluation_Committee"
    ADMIN = "Admin"
    SUPERADMIN = "SuperAdmin"

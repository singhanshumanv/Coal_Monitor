from pydantic import BaseModel
from datetime import date

class ComplianceTask(BaseModel):
    task_id: int
    project_id: int
    compliance_type: str
    deadline: date
    status: str
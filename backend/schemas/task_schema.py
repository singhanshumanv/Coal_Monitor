from pydantic import BaseModel
from datetime import date


class TaskCreate(BaseModel):

    project_id: int
    compliance_type: str
    deadline: date
    status: str


class TaskUpdate(BaseModel):

    status: str
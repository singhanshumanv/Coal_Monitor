from pydantic import BaseModel
from datetime import date

class ProjectCreate(BaseModel):
    name: str
    location: str
    owner: str
    start_date: date
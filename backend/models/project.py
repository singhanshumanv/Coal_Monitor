from sqlalchemy import Column, Integer, String, Date
from .base import Base

class Project(Base):

    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    location = Column(String(100))
    owner = Column(String(100))
    start_date = Column(Date)
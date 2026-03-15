from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from .base import Base


class Task(Base):

    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.project_id"))

    compliance_type = Column(Text)

    deadline = Column(Date)

    status = Column(String(50), default="Pending")
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from .base import Base


class Report(Base):

    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.project_id"))

    report_path = Column(String(300))

    created_at = Column(DateTime, default=datetime.utcnow)
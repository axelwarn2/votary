from backend.utlis.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class ProjectModel(Base):
    __tablename__ = "Project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
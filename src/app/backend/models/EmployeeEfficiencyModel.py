from backend.utlis.db import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from datetime import datetime

class EmployeeEfficiencyModel(Base):
    __tablename__ = "EmployeeEfficiency"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("Employee.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    efficiency = Column(Float, nullable=False)
    count_task = Column(Integer, nullable=False)
    complete = Column(Integer, nullable=False)
    expired = Column(Integer, nullable=False)
    calculated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from backend.utlis.db import Base
from datetime import datetime

class EmployeeEfficiencyModel(Base):
    __tablename__ = "EmployeeEfficiency"

    employee_id = Column(Integer, ForeignKey("Employee.id", ondelete="CASCADE"), primary_key=True, comment="Идентификатор сотрудника")
    efficiency = Column(Float, nullable=False, comment="Процент эффективности")
    count_task = Column(Integer, nullable=False, comment="Общее количество поручений")
    completed = Column(Integer, nullable=False, comment="Количество выполненных поручений")
    expired = Column(Integer, nullable=False, comment="Количество просроченных поручений")
    calculated_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="Дата вычисления")
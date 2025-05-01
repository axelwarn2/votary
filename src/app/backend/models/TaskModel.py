import enum
from backend.utlis.db import Base
from sqlalchemy import Column, Integer, TIMESTAMP, String, Enum, ForeignKey

class StatusEnum(str, enum.Enum):
    выполняется = "выполняется"
    выполнена = "выполнена"

class TaskModel(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(TIMESTAMP, nullable=False)
    deadline = Column(TIMESTAMP, nullable=True)
    description = Column(String(1000), nullable=False)
    mark = Column(Integer, nullable=True)
    status = Column(Enum(StatusEnum), nullable=False)
    employee_id = Column(Integer, ForeignKey("Employee.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    meeting_id = Column(Integer, ForeignKey("Meeting.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

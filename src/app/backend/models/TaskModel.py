import enum
from sqlalchemy import Column, Integer, String, TIMESTAMP, DateTime, Enum, ForeignKey
from backend.utlis.db import Base

class StatusEnum(str, enum.Enum):
    выполняется = "выполняется"
    выполнена = "выполнена"

class UrgencyEnum(str, enum.Enum):
    да = "да"
    нет = "нет"

class TaskModel(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True, index=True, comment="Идентификатор поручения")
    date_created = Column(TIMESTAMP, nullable=False, default="CURRENT_TIMESTAMP", comment="Дата создания")
    deadline = Column(DateTime, comment="Срок выполнения")
    description = Column(String(1000), nullable=False, comment="Описание")
    status = Column(Enum(StatusEnum), nullable=False, comment="Статус")
    urgency = Column(Enum(UrgencyEnum), nullable=False, default="нет", comment="Срочность")
    employee_id = Column(Integer, ForeignKey("Employee.id", ondelete="CASCADE"), nullable=False, comment="Сотрудник (исполнитель)")
    meeting_id = Column(Integer, ForeignKey("Meeting.id", ondelete="CASCADE"), nullable=False, comment="Собрание")
    leader_id = Column(Integer, ForeignKey("Employee.id", ondelete="CASCADE"), nullable=False, comment="Сотрудник (руководитель)")
    project_id = Column(Integer, ForeignKey("Project.id", ondelete="SET NULL"), comment="Проект")
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    выполняется = "выполняется"
    выполнена = "выполнена"

class UrgencyEnum(str, Enum):
    да = "да"
    нет = "нет"

class TaskCreate(BaseModel):
    description: str
    deadline: Optional[datetime] = None
    urgency: Optional[UrgencyEnum] = UrgencyEnum.нет
    employee_id: int
    meeting_id: int
    leader_id: int
    project_id: Optional[int] = None

class TaskRead(BaseModel):
    id: int
    date_created: datetime
    deadline: Optional[datetime]
    description: str
    status: StatusEnum
    urgency: UrgencyEnum
    employee_id: int
    meeting_id: int
    employee_surname: str
    employee_name: str
    leader_id: int
    leader_surname: Optional[str]
    leader_name: Optional[str]
    project_id: Optional[int]

    class Config:
        orm_mode = True

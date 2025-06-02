from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskRead(BaseModel):
    id: int
    date_created: datetime
    deadline: Optional[datetime] = None
    description: str
    status: str
    employee_id: int
    meeting_id: int
    employee_surname: str
    employee_name: str
    leader_id: int
    leader_surname: str
    leader_name: str
    project_id: Optional[int]

    class Config:
        orm_mode = True

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskRead(BaseModel):
    id: int
    date_created: datetime
    deadline: Optional[datetime] = None
    description: str
    mark: Optional[int] = None
    status: str
    employee_id: int
    meeting_id: int
    employee_surname: str
    employee_name: str

    class Config:
        orm_mode = True
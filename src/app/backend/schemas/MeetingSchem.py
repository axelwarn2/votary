from pydantic import BaseModel
from datetime import datetime, time

class MeetingRead(BaseModel):
    id: int
    date_event: datetime
    time_start: time
    time_end: time
    text: str

    class Config:
        orm_mode = True

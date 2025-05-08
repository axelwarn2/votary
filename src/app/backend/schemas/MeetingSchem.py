from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

class MeetingRead(BaseModel):
    id: int
    date_event: datetime
    time_start: time
    time_end: time
    text: str
    audio_path: Optional[str] = None

    class Config:
        orm_mode = True

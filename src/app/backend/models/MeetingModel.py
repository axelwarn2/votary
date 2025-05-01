from backend.utlis.db import Base
from sqlalchemy import Column, Integer, TIMESTAMP, Time, Text

class MeetingModel(Base):
    __tablename__ = "Meeting"

    id = Column(Integer, primary_key=True, index=True)
    date_event = Column(TIMESTAMP, nullable=False)
    time_start = Column(Time, nullable=False)
    time_end = Column(Time, nullable=False)
    text = Column(Text, nullable=False)

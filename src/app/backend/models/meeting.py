from sqlalchemy import Column, Integer, String, Time, TIMESTAMP, Text
from backend.utlis.db import Base

class Meeting(Base):
    __tablename__ = "Meeting"

    id = Column(Integer, primary_key=True, index=True)
    date_event = Column(TIMESTAMP, nullable=False)
    time_start = Column(Time, nullable=False)
    time_end = Column(Time, nullable=False)
    text = Column(Text, nullable=False)

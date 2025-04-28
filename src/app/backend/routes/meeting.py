from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.meeting import Meeting
from backend.utlis.db import get_db
from backend.schemas.meeting import MeetingRead

router = APIRouter()

@router.get("/meetings", response_model=list[MeetingRead])
def get_meetings(db: Session = Depends(get_db)):
    meetings = db.query(Meeting).all()
    return meetings

@router.get("/meetings/{meeting_id}", response_model=MeetingRead)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    return meeting
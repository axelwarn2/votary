from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.MeetingSchem import MeetingRead
from backend.utlis.db import get_db
from backend.models.MeetingModel import MeetingModel

router = APIRouter()

@router.get("/meetings", response_model=list[MeetingRead])
def get_meetings(db: Session = Depends(get_db)):
    meetings = db.query(MeetingModel).all()
    return meetings

@router.get("/meetings/{meeting_id}", response_model=MeetingRead)
def get_meeting_by_id(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(MeetingModel).filter(MeetingModel.id == meeting_id).first()
    return meeting

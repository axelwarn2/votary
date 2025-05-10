from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.MeetingSchem import MeetingRead
from backend.utlis.db import get_db
from backend.repositories.MeetingRepository import MeetingRepository
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/meetings", response_model=list[MeetingRead])
def get_meetings(db: Session = Depends(get_db)):
    repository = MeetingRepository(db)
    return repository.get_all_meetings()

@router.get("/meetings/{meeting_id}", response_model=MeetingRead)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    repository = MeetingRepository(db)
    return repository.get_meeting_by_id(meeting_id)

@router.get("/meetings/{meeting_id}/audio")
async def download_meeting_audio(meeting_id: int, db: Session = Depends(get_db)):
    repository = MeetingRepository(db)
    meeting = repository.get_meeting_by_id(meeting_id)
    return FileResponse(
        path=meeting.audio_path,
        filename=os.path.basename(meeting.audio_path),
        media_type="audio/wav"
    )

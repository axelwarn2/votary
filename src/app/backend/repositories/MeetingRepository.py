from backend.models.MeetingModel import MeetingModel
from typing import Optional

class MeetingRepository:
    def __init__(self, db):
        self.db = db

    def get_all_meetings(self, date_from: Optional[str] = None, date_to: Optional[str] = None):
        query = self.db.query(MeetingModel)
        if date_from:
            query = query.filter(MeetingModel.date_event >= date_from)
        if date_to:
            query = query.filter(MeetingModel.date_event <= date_to)
        meetings = query.all()
        return meetings

    def get_meeting_by_id(self, meeting_id):
        meeting = self.db.query(MeetingModel).filter(MeetingModel.id == meeting_id).first()
        return meeting

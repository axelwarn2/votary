from backend.models.MeetingModel import MeetingModel

class MeetingRepository:
    def __init__(self, db):
        self.db = db

    def get_all_meetings(self):
        meetings = self.db.query(MeetingModel).all()
        return meetings

    def get_meeting_by_id(self, meeting_id):
        meeting = self.db.query(MeetingModel).filter(MeetingModel.id == meeting_id).first()
        return meeting

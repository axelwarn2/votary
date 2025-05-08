from uuid import uuid4
from typing import Dict, Optional
from fastapi import Response

sessions: Dict[str, dict] = {}

def create_session(employee: dict):
    session_id = str(uuid4())
    sessions[session_id] = {
        "employee": employee,
    }
    return session_id

def get_session(session_id: str):
    return sessions.get(session_id)

def delete_session(session_id: str):
    sessions.pop(session_id, None)
    
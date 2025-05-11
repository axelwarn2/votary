from fastapi import HTTPException
from backend.utlis.session import create_session, get_session, delete_session
from backend.models.EmployeeModel import EmployeeModel
import bcrypt

def login_in_program(login_data, response, db):
    employee = db.query(EmployeeModel).filter(EmployeeModel.email == login_data.email).first()
    if not employee:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not bcrypt.checkpw(login_data.password.encode('utf-8'), employee.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    session_id = create_session({
        "id": employee.id,
        "surname": employee.surname,
        "name": employee.name,
        "lastname": employee.lastname,
        "email": employee.email,
        "role": employee.role
    })

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800,
        path="/"
    )

    return {"message": "Успешный вход", "session_id": session_id}

def get_current_user_from_session(session_id, db=None):
    session = get_session(session_id)
    if not session or "employee" not in session:
        raise HTTPException(status_code=401, detail="Invalid session")
    return session["employee"]

def logout_from_program(response, session_id):
    if session_id:
        delete_session(session_id)

    response.delete_cookie("session_id")
    return {"message": "Успешный выход"}

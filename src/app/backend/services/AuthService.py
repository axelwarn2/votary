from backend.utlis.session import create_session, get_session, delete_session
from backend.models.EmployeeModel import EmployeeModel

def login_in_program(login_data, response, db):
    employee = db.query(EmployeeModel).filter(EmployeeModel.email == login_data.email).first()

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
        max_age=1800
    )

    return {"message": "Успешный вход"}

def get_current_user_from_session(session_id):
    session = get_session(session_id)
    return session["employee"]

def logout_from_program(response, session_id):
    if session_id:
        delete_session(session_id)

    response.delete_cookie("session_id")
    return {"message": "Успешный выход"}

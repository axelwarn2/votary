from fastapi import APIRouter, Depends, Response, Cookie, HTTPException
from backend.schemas.EmployeeSchem import EmployeeCreate, EmployeeStats, EmployeeLogin
from backend.schemas.InvitationRegister import InvitationCreate
from backend.models.EmployeeModel import EmployeeModel
from backend.services.EmailService import EmailService
from sqlalchemy.orm import Session
from backend.utlis.db import get_db
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.services.AuthService import login_in_program, get_current_user_from_session, logout_from_program
from typing import Optional

router = APIRouter()

@router.post("/employee")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing_employee = db.query(EmployeeModel).filter(EmployeeModel.email == employee.email).first()
    if existing_employee:
        raise HTTPException(status_code=400, detail="Employee with this email already exists")
    
    repository = EmployeeRepository(db)
    return repository.create_employee(employee)

@router.get("/employees", response_model=list[EmployeeStats])
def get_employees(db: Session = Depends(get_db)):
    repository = EmployeeRepository(db)
    return repository.get_all_employees()

@router.get("/employees/{employee_id}", response_model=EmployeeStats)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    repository = EmployeeRepository(db)
    return repository.get_employee_by_id(employee_id)

@router.post("/login")
def login(login_data: EmployeeLogin, response: Response, db: Session = Depends(get_db)):
    return login_in_program(login_data, response, db)

@router.get("/me")
def get_current_user(session_id: Optional[str] = Cookie(None)):
    return get_current_user_from_session(session_id)

@router.post("/logout")
def logout(response: Response, session_id: Optional[str] = Cookie(None)):
    return logout_from_program(response, session_id)

@router.post("/invitation")
def create_invitation(invitation: InvitationCreate, session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    user = get_current_user_from_session(session_id)
    if user.get("role") != "руководитель":
        raise HTTPException(status_code=403, detail="Only leaders can send invitations")

    existing_employee = db.query(EmployeeModel).filter(EmployeeModel.email == invitation.email).first()
    if existing_employee:
        raise HTTPException(status_code=400, detail="Сотрудник с таким адресом почту уже существует")

    email_service = EmailService(db)
    email_service.send_invitation_email(invitation.email, user["id"])

    return {"message": f"Invitation sent to {invitation.email}"}

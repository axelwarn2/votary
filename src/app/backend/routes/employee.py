from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.employee import Employee
from backend.utlis.db import get_db
from backend.schemas.employee import EmployeeCreate

router = APIRouter()

@router.post("/employee/")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(
        surname=employee.surname,
        name=employee.name,
        lastname=employee.lastname,
        email=employee.email,
        password=employee.password,
        role=employee.role
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee
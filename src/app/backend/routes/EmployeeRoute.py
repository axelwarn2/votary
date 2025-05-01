from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.EmployeeModel import EmployeeModel
from backend.schemas.EmployeeSchem import EmployeeCreate, EmployeeStats
from backend.utlis.db import get_db
from backend.models.TaskModel import TaskModel, StatusEnum
from sqlalchemy import select, func, case
from datetime import datetime
import random

router = APIRouter()

@router.post("/employee")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = EmployeeModel(
        surname = employee.surname,
        name = employee.name,
        lastname = employee.lastname,
        email = employee.email,
        password = employee.password,
        role = employee.role
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/employees", response_model=list[EmployeeStats])
def get_employee_stats(db: Session = Depends(get_db)):
    current_date = datetime(2025, 4, 30)
    stmt = (
        select(
            EmployeeModel.id,
            EmployeeModel.surname,
            EmployeeModel.name,
            func.count(TaskModel.id).label("count_task"),
            func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("complete"),
            func.sum(case((TaskModel.deadline < current_date, 1), else_=0)).label("expired"),
        )
        .outerjoin(TaskModel, EmployeeModel.id == TaskModel.employee_id)
        .group_by(EmployeeModel.id, EmployeeModel.surname, EmployeeModel.name)
    )
    result = db.execute(stmt).all()

    employees_stats = [
        {
            "id": row.id,
            "surname": row.surname,
            "name": row.name,
            "count_task": row.count_task,
            "complete": row.complete,
            "expired": row.expired,
            "efficiency": f"{random.randint(10, 100)}%"
        }
        for row in result
    ] 
    return employees_stats

@router.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    current_date = datetime(2025, 4, 30)
    stmt = (
        select(
            EmployeeModel.id,
            EmployeeModel.surname,
            EmployeeModel.name,
            func.count(TaskModel.id).label("count_task"),
            func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("complete"),
            func.sum(case((TaskModel.deadline < current_date, 1), else_=0)).label("expired"),
        )
        .outerjoin(TaskModel, EmployeeModel.id == TaskModel.employee_id)
        .where(EmployeeModel.id == employee_id)
        .group_by(EmployeeModel.id, EmployeeModel.surname, EmployeeModel.name)
    )
    result = db.execute(stmt).first()

    return {
        "id": result.id,
        "surname": result.surname,
        "name": result.name,
        "count_task": result.count_task,
        "complete": result.complete,
        "expired": result.expired,
        "efficiency": f"{random.randint(10, 100)}%"
    }

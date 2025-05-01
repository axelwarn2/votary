from fastapi import APIRouter, Depends
from backend.schemas.TaskSchem import TaskRead
from sqlalchemy.orm import Session
from backend.utlis.db import get_db
from sqlalchemy import select
from backend.models.TaskModel import TaskModel
from backend.models.EmployeeModel import EmployeeModel

router = APIRouter()

@router.get("/tasks", response_model=list[TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    stmt = select(TaskModel, EmployeeModel).join(EmployeeModel, TaskModel.employee_id == EmployeeModel.id)
    result = db.execute(stmt).all()
    
    tasks = [
        {
            "id": task.id,
            "date_created": task.date_created,
            "deadline": task.deadline,
            "description": task.description,
            "mark": task.mark,
            "status": task.status,
            "employee_id": task.employee_id,
            "meeting_id": task.meeting_id,
            "employee_surname": employee.surname,
            "employee_name": employee.name
        }
        for task, employee in result
    ]
    return tasks

@router.get("/tasks/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    stmt = select(TaskModel, EmployeeModel).join(EmployeeModel, TaskModel.employee_id == EmployeeModel.id).where(TaskModel.id == task_id)
    result = db.execute(stmt).first()

    task, employee = result
    return {
        "id": task.id,
        "date_created": task.date_created,
        "deadline": task.deadline,
        "description": task.description,
        "mark": task.mark,
        "status": task.status,
        "employee_id": task.employee_id,
        "meeting_id": task.meeting_id,
        "employee_surname": employee.surname,
        "employee_name": employee.name
    }

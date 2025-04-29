from backend.utlis.db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.task import Task
from backend.models.employee import Employee
from backend.schemas.task import TaskRead
from sqlalchemy import select

router = APIRouter()

@router.get("/tasks", response_model=list[TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    stmt = select(Task, Employee).join(Employee, Task.employee_id == Employee.id)
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

@router.get("/task/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    stmt = select(Task, Employee).join(Employee, Task.employee_id == Employee.id).where(Task.id == task_id)
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
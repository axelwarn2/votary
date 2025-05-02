from fastapi import APIRouter, Depends
from backend.schemas.TaskSchem import TaskRead
from sqlalchemy.orm import Session
from backend.utlis.db import get_db
from backend.repositories.TaskRepository import TaskRepository

router = APIRouter()

@router.get("/tasks", response_model=list[TaskRead])
def get_tasks(db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    return repository.get_all_tasks()

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    return repository.get_task_by_id(task_id)

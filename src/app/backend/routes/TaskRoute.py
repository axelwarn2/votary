from fastapi import APIRouter, Depends, HTTPException
from backend.schemas.TaskSchem import TaskRead
from sqlalchemy.orm import Session
from backend.utlis.db import get_db
from backend.repositories.TaskRepository import TaskRepository

router = APIRouter()

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    try:
        return repository.get_all_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    return repository.get_task_by_id(task_id)

@router.get("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    
    success = repository.complete_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Task not found or already completed")

from fastapi import APIRouter, Depends, HTTPException
from backend.schemas.TaskSchem import TaskRead
from sqlalchemy.orm import Session
from backend.utlis.db import get_db
from backend.repositories.TaskRepository import TaskRepository
from typing import Optional, List

router = APIRouter()

@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    status: Optional[str] = None,
    project_id: Optional[int] = None,
    employee_ids: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    urgency: Optional[str] = None,
    db: Session = Depends(get_db)
):
    repository = TaskRepository(db)
    try:
        # Преобразование строки employee_ids в список целых чисел
        employee_ids_list = [int(eid) for eid in employee_ids.split(',')] if employee_ids else None
        tasks = repository.get_all_tasks(
            status=status,
            project_id=project_id,
            employee_ids=employee_ids_list,
            date_from=date_from,
            date_to=date_to,
            urgency=urgency
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    return repository.get_task_by_id(task_id)

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    success = repository.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.get("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    
    success = repository.complete_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Task not found or already completed")

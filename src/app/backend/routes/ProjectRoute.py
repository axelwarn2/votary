from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.utlis.db import get_db
from backend.repositories.ProjectRepository import ProjectRepository
from backend.repositories.TaskRepository import TaskRepository
from backend.models.ProjectModel import ProjectModel
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

router = APIRouter()

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_tasks: int
    incomplete_tasks: int

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

class TaskStatusUpdate(BaseModel):
    status: str

@router.post("/project", response_model=ProjectRead)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    repository = ProjectRepository(db)
    existing_project = db.query(ProjectModel).filter(ProjectModel.name == project.name).first()
    if existing_project:
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    new_project = repository.create_project(project.name, project.description)
    return {
        "id": new_project.id,
        "name": new_project.name,
        "description": new_project.description,
        "created_at": new_project.created_at,
        "updated_at": new_project.updated_at,
        "completed_tasks": 0,
        "incomplete_tasks": 0
    }

@router.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    repository = ProjectRepository(db)
    existing_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.name != existing_project.name:
        duplicate_project = db.query(ProjectModel).filter(ProjectModel.name == project.name).first()
        if duplicate_project:
            raise HTTPException(status_code=400, detail="Project with this name already exists")
    updated_project = repository.update_project(project_id, project.name, project.description)
    return {
        "id": updated_project.id,
        "name": updated_project.name,
        "description": updated_project.description,
        "created_at": updated_project.created_at,
        "updated_at": updated_project.updated_at,
        "completed_tasks": 0,
        "incomplete_tasks": 0
    }

@router.get("/projects", response_model=list[ProjectRead])
def get_projects(db: Session = Depends(get_db)):
    repository = ProjectRepository(db)
    return repository.get_all_projects()

@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    repository = ProjectRepository(db)
    project = repository.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/tasks/{task_id}/status")
def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    task = repository.update_task_status(task_id, status_update.status)
    return {
        "id": task.id,
        "status": task.status
    }

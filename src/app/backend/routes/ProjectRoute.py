from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.utlis.db import get_db
from backend.repositories.ProjectRepository import ProjectRepository
from backend.models.ProjectModel import ProjectModel
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

router = APIRouter()

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

@router.post("/projects", response_model=ProjectRead)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    repository = ProjectRepository(db)
    existing_project = db.query(ProjectModel).filter(ProjectModel.name == project.name).first()
    if existing_project:
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    return repository.create_project(project.name, project.description)

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

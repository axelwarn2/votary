from sqlalchemy import select, func
from sqlalchemy.sql.expression import case
from backend.models.ProjectModel import ProjectModel
from backend.models.TaskModel import TaskModel, StatusEnum
from datetime import datetime

class ProjectRepository:
    def __init__(self, db):
        self.db = db

    def create_project(self, name: str, description: str = None):
        new_project = ProjectModel(name=name, description=description)
        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project)
        return new_project

    def update_project(self, project_id: int, name: str, description: str = None):
        project = self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        if not project:
            return None
        project.name = name
        project.description = description
        project.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_all_projects(self):
        stmt = (
            select(
                ProjectModel,
                func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("completed_tasks"),
                func.sum(case((TaskModel.status != StatusEnum.выполнена, 1), else_=0)).label("incomplete_tasks")
            )
            .outerjoin(TaskModel, ProjectModel.id == TaskModel.project_id)
            .group_by(ProjectModel.id)
        )
        result = self.db.execute(stmt).all()
        projects = [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
                "completed_tasks": completed or 0,
                "incomplete_tasks": incomplete or 0
            }
            for project, completed, incomplete in result
        ]
        return projects

    def get_project_by_id(self, project_id: int):
        stmt = (
            select(
                ProjectModel,
                func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("completed_tasks"),
                func.sum(case((TaskModel.status != StatusEnum.выполнена, 1), else_=0)).label("incomplete_tasks")
            )
            .outerjoin(TaskModel, ProjectModel.id == TaskModel.project_id)
            .where(ProjectModel.id == project_id)
            .group_by(ProjectModel.id)
        )
        result = self.db.execute(stmt).first()
        if not result:
            return None
        project, completed, incomplete = result
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "completed_tasks": completed or 0,
            "incomplete_tasks": incomplete or 0
        }
    
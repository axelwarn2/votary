from sqlalchemy import select
from backend.models.ProjectModel import ProjectModel

class ProjectRepository:
    def __init__(self, db):
        self.db = db

    def create_project(self, name: str, description: str = None):
        new_project = ProjectModel(name=name, description=description)
        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project)
        return new_project

    def get_all_projects(self):
        return self.db.query(ProjectModel).all()

    def get_project_by_id(self, project_id: int):
        return self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
from sqlalchemy import select, func, update
from sqlalchemy.orm import aliased
from backend.models.TaskModel import TaskModel, StatusEnum
from backend.models.EmployeeModel import EmployeeModel
from fastapi import HTTPException
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskRepository:
    def __init__(self, db):
        self.db = db

    def get_all_tasks(self, status: Optional[str] = None, project_id: Optional[int] = None):
        logger.info(f"Fetching tasks with status={status}, project_id={project_id}")
        EmployeeResponsible = aliased(EmployeeModel, name="employee_responsible")
        EmployeeLeader = aliased(EmployeeModel, name="employee_leader")

        stmt = select(TaskModel, EmployeeResponsible, EmployeeLeader).join(
            EmployeeResponsible, TaskModel.employee_id == EmployeeResponsible.id
        ).join(
            EmployeeLeader, TaskModel.leader_id == EmployeeLeader.id, isouter=True
        )

        if status:
            stmt = stmt.where(TaskModel.status == status)
        if project_id is not None:
            stmt = stmt.where(TaskModel.project_id == project_id)

        logger.info(f"SQL Query: {stmt}")
        result = self.db.execute(stmt).all()

        tasks = [
            {
                "id": task.id,
                "date_created": task.date_created,
                "deadline": task.deadline,
                "description": task.description,
                "status": task.status,
                "employee_id": task.employee_id,
                "meeting_id": task.meeting_id,
                "employee_surname": employee.surname,
                "employee_name": employee.name,
                "leader_id": task.leader_id,
                "leader_surname": leader.surname if leader else None,
                "leader_name": leader.name if leader else None,
                "project_id": task.project_id
            }
            for task, employee, leader in result
        ]
        logger.info(f"Returning {len(tasks)} tasks")
        return sorted(tasks, key=lambda x: x["id"])

    def get_task_by_id(self, task_id):
        EmployeeResponsible = aliased(EmployeeModel, name="employee_responsible")
        EmployeeLeader = aliased(EmployeeModel, name="employee_leader")

        stmt = select(TaskModel, EmployeeResponsible, EmployeeLeader).join(
            EmployeeResponsible, TaskModel.employee_id == EmployeeResponsible.id
        ).join(
            EmployeeLeader, TaskModel.leader_id == EmployeeLeader.id, isouter=True
        ).where(TaskModel.id == task_id)
        result = self.db.execute(stmt).first()

        if not result:
            raise HTTPException(status_code=404, detail="Task not found")

        task, employee, leader = result
        return {
            "id": task.id,
            "date_created": task.date_created,
            "deadline": task.deadline,
            "description": task.description,
            "status": task.status,
            "employee_id": task.employee_id,
            "meeting_id": task.meeting_id,
            "employee_surname": employee.surname,
            "employee_name": employee.name,
            "leader_id": task.leader_id,
            "leader_surname": leader.surname if leader else None,
            "leader_name": leader.name if leader else None,
            "project_id": task.project_id
        }

    def create_task(self, task):
        new_task = TaskModel(
            description=task.description,
            deadline=task.deadline,
            status=StatusEnum.выполняется,
            employee_id=task.employee_id,
            meeting_id=task.meeting_id,
            leader_id=task.leader_id,
            project_id=task.project_id
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def update_task(self, task_id, task_update):
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        for key, value in task_update.dict(exclude_unset=True).items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task_status(self, task_id: int, status: str):
        logger.info(f"Attempting to update task {task_id} to status {status}")
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail="Task not found")
        if status not in [e.value for e in StatusEnum]:
            logger.error(f"Invalid status: {status}")
            raise HTTPException(status_code=400, detail="Invalid status")
        logger.info(f"Current task status: {task.status}")
        # Используем явный UPDATE вместо присваивания
        self.db.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(status=status)
        )
        logger.info(f"Executed UPDATE for task {task_id} to status {status}")
        try:
            self.db.commit()
            logger.info(f"Committed task {task_id} with status {status}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to commit task {task_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")
        self.db.refresh(task)
        logger.info(f"Refreshed task {task_id}: {task.status}")
        return task

    def delete_task(self, task_id):
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        self.db.delete(task)
        self.db.commit()
        return True
    
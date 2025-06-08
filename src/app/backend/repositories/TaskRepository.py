from sqlalchemy import select, func, update
from sqlalchemy.orm import aliased
from backend.models.TaskModel import TaskModel, StatusEnum
from backend.models.EmployeeModel import EmployeeModel
from fastapi import HTTPException
from typing import Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskRepository:
    def __init__(self, db):
        self.db = db

    def get_all_tasks(
        self,
        status: Optional[str] = None,
        project_id: Optional[int] = None,
        employee_ids: Optional[List[int]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        urgency: Optional[str] = None
    ):
        logger.info(f"Fetching tasks with status={status}, project_id={project_id}, employee_ids={employee_ids}, date_from={date_from}, date_to={date_to}, urgency={urgency}")
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
        if employee_ids:
            stmt = stmt.where(TaskModel.employee_id.in_(employee_ids))
        if date_from:
            stmt = stmt.where(TaskModel.date_created >= date_from)
        if date_to:
            stmt = stmt.where(TaskModel.date_created <= date_to)
        if urgency:
            stmt = stmt.where(TaskModel.urgency == urgency)

        stmt = stmt.order_by(
            TaskModel.urgency.desc(),
            TaskModel.status.asc(),
            TaskModel.id
        )

        logger.info(f"SQL Query: {stmt}")
        try:
            result = self.db.execute(stmt).all()
        except Exception as e:
            logger.error(f"Failed to fetch tasks: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch tasks")

        tasks = [
            {
                "id": task.id,
                "date_created": task.date_created,
                "deadline": task.deadline,
                "description": task.description,
                "status": task.status,
                "urgency": task.urgency.value if task.urgency else "нет",
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
        logger.info(f"Returning {len(tasks)} tasks: {[t['id'] for t in tasks]}")
        return tasks

    def get_task_by_id(self, task_id):
        EmployeeResponsible = aliased(EmployeeModel, name="employee_responsible")
        EmployeeLeader = aliased(EmployeeModel, name="employee_leader")

        stmt = select(TaskModel, EmployeeResponsible, EmployeeLeader).join(
            EmployeeResponsible, TaskModel.employee_id == EmployeeResponsible.id
        ).join(
            EmployeeLeader, TaskModel.leader_id == EmployeeLeader.id, isouter=True
        ).where(TaskModel.id == task_id)

        try:
            result = self.db.execute(stmt).first()
        except Exception as e:
            logger.error(f"Failed to fetch task {task_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch task")

        if not result:
            raise HTTPException(status_code=404, detail="Task not found")

        task, employee, leader = result
        return {
            "id": task.id,
            "date_created": task.date_created,
            "deadline": task.deadline,
            "description": task.description,
            "status": task.status,
            "urgency": task.urgency.value if task.urgency else "нет",
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
            urgency=task.urgency or 'нет',
            employee_id=task.employee_id,
            meeting_id=task.meeting_id,
            leader_id=task.leader_id,
            project_id=task.project_id
        )
        try:
            self.db.add(new_task)
            self.db.commit()
            self.db.refresh(new_task)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create task: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create task")
        return new_task

    def update_task(self, task_id, task_update):
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        for key, value in task_update.dict(exclude_unset=True).items():
            setattr(task, key, value)
        try:
            self.db.commit()
            self.db.refresh(task)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update task {task_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to update task")
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
        try:
            self.db.execute(
                update(TaskModel)
                .where(TaskModel.id == task_id)
                .values(status=status)
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update task {task_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")
        self.db.refresh(task)
        return task

    def delete_task(self, task_id):
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        try:
            self.db.delete(task)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete task {task_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete task")
        return True
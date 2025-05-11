from sqlalchemy import select, func, update
from sqlalchemy.orm import aliased
from backend.models.TaskModel import TaskModel, StatusEnum
from backend.models.EmployeeModel import EmployeeModel
from datetime import date, timedelta

class TaskRepository:
    def __init__(self, db):
        self.db = db

    def get_all_tasks(self):
        EmployeeResponsible = aliased(EmployeeModel, name="employee_responsible")
        EmployeeLeader = aliased(EmployeeModel, name="employee_leader")

        stmt = select(TaskModel, EmployeeResponsible, EmployeeLeader).join(
            EmployeeResponsible, TaskModel.employee_id == EmployeeResponsible.id
        ).join(
            EmployeeLeader, TaskModel.leader_id == EmployeeLeader.id, isouter=True
        )
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
                "leader_surname": leader.surname,
                "leader_name": leader.name
            }
            for task, employee, leader in result
        ]
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
            "leader_name": leader.name if leader else None
        }
    
    def get_tasks_due_tomorrow(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        EmployeeResponsible = aliased(EmployeeModel, name="employee_responsible")
        EmployeeLeader = aliased(EmployeeModel, name="employee_leader")

        stmt = select(TaskModel, EmployeeResponsible, EmployeeLeader).join(
            EmployeeResponsible, TaskModel.employee_id == EmployeeResponsible.id
        ).join(
            EmployeeLeader, TaskModel.leader_id == EmployeeLeader.id, isouter=True
        ).where(
            func.date(TaskModel.deadline) == tomorrow,
            TaskModel.status == StatusEnum.выполняется
        )
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
                "leader_name": leader.name if leader else None
            }
            for task, employee, leader in result
        ]
        return tasks

    def complete_task(self, task_id: int):
        stmt = select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.status == StatusEnum.выполняется
        )
        task = self.db.execute(stmt).scalar_one_or_none()
        if not task:
            return False
        update_stmt = update(TaskModel).where(
            TaskModel.id == task_id
        ).values(status=StatusEnum.выполнена)
        self.db.execute(update_stmt)
        self.db.commit()
        return True
    
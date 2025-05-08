from sqlalchemy import select
from sqlalchemy.orm import aliased
from backend.models.TaskModel import TaskModel
from backend.models.EmployeeModel import EmployeeModel

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
                "mark": task.mark,
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
        return tasks

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
            "mark": task.mark,
            "status": task.status,
            "employee_id": task.employee_id,
            "meeting_id": task.meeting_id,
            "employee_surname": employee.surname,
            "employee_name": employee.name,
            "leader_id": task.leader_id,
            "leader_surname": leader.surname,
            "leader_name": leader.name
        }
    
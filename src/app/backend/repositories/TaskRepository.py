from sqlalchemy import select
from backend.models.TaskModel import TaskModel
from backend.models.EmployeeModel import EmployeeModel

class TaskRepository:
    def __init__(self, db):
        self.db = db

    def get_all_tasks(self):
        stmt = select(TaskModel, EmployeeModel).join(EmployeeModel, TaskModel.employee_id == EmployeeModel.id)
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
                "employee_name": employee.name
            }
            for task, employee in result
        ]
        return tasks

    def get_task_by_id(self, task_id):
        stmt = select(TaskModel, EmployeeModel).join(EmployeeModel, TaskModel.employee_id == EmployeeModel.id).where(TaskModel.id == task_id)
        result = self.db.execute(stmt).first()

        task, employee = result
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
            "employee_name": employee.name
        }

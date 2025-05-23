from backend.models.EmployeeModel import EmployeeModel
from backend.models.TaskModel import TaskModel, StatusEnum
from sqlalchemy import select, func, case
from datetime import date
import bcrypt

class EmployeeRepository:
    def __init__(self, db):
        self.db = db

    def create_employee(self, employee):
        new_employee = EmployeeModel(
            surname = employee.surname,
            name = employee.name,
            lastname = employee.lastname,
            email = employee.email,
            password = bcrypt.hashpw(employee.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            role = employee.role
        )

        self.db.add(new_employee)
        self.db.commit()
        self.db.refresh(new_employee)

        return new_employee

    def get_all_employees(self):
        current_date = date.today()
        stmt = (
            select(
                EmployeeModel.id,
                EmployeeModel.surname,
                EmployeeModel.name,
                EmployeeModel.email,
                func.count(TaskModel.id).label("count_task"),
                func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("complete"),
                func.sum(case((TaskModel.deadline < current_date, 1), else_=0)).label("expired"),
            )
            .outerjoin(TaskModel, EmployeeModel.id == TaskModel.employee_id)
            .group_by(EmployeeModel.id, EmployeeModel.surname, EmployeeModel.name, EmployeeModel.email)
        )
        result = self.db.execute(stmt).all()

        employees_stats = [
            {
                "id": row.id,
                "surname": row.surname,
                "name": row.name,
                "email": row.email,
                "count_task": row.count_task,
                "complete": row.complete,
                "expired": row.expired,
                "efficiency": (
                    f"{round(100 - (row.expired / row.count_task) * 100)}%"
                    if row.count_task != 0 else "100%"
                )
            }
            for row in result
        ]
        return sorted(employees_stats, key=lambda x: x["id"])

    def get_employee_by_id(self, employee_id):
        current_date = date.today()
        stmt = (
            select(
                EmployeeModel.id,
                EmployeeModel.surname,
                EmployeeModel.name,
                EmployeeModel.email,
                func.count(TaskModel.id).label("count_task"),
                func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("complete"),
                func.sum(case((TaskModel.deadline < current_date, 1), else_=0)).label("expired"),
            )
            .outerjoin(TaskModel, EmployeeModel.id == TaskModel.employee_id)
            .where(EmployeeModel.id == employee_id)
            .group_by(EmployeeModel.id, EmployeeModel.surname, EmployeeModel.name, EmployeeModel.email)
        )
        result = self.db.execute(stmt).first()

        return {
            "id": result.id,
            "surname": result.surname,
            "name": result.name,
            "email": result.email,
            "count_task": result.count_task,
            "complete": result.complete,
            "expired": result.expired,
            "efficiency": (
                f"{round(100 - (result.expired / result.count_task) * 100)}%"
                if result.count_task != 0 else "100%"
            )
        }

    def get_employee_by_email(self, email: str):
        return self.db.query(EmployeeModel).filter(EmployeeModel.email == email).first()

    def update_employee_password(self, employee_id: int, new_password: str):
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
        if not employee:
            return None
        employee.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.db.commit()
        return employee

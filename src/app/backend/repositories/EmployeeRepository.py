from backend.models.EmployeeModel import EmployeeModel
from backend.models.TaskModel import TaskModel, StatusEnum
from backend.models.EmployeeEfficiencyModel import EmployeeEfficiencyModel
from sqlalchemy import select, func, case
from datetime import date
import bcrypt

class EmployeeRepository:
    def __init__(self, db):
        self.db = db

    def create_employee(self, employee):
        new_employee = EmployeeModel(
            surname=employee.surname,
            name=employee.name,
            lastname=employee.lastname,
            email=employee.email,
            password=bcrypt.hashpw(employee.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            role=employee.role,
            birth_date=employee.birth_date,
            is_on_sick_leave=False,
            is_on_vacation=False
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
                EmployeeModel.is_on_sick_leave,
                EmployeeModel.is_on_vacation,
                func.count(TaskModel.id).label("count_task"),
                func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("complete"),
                func.sum(case((TaskModel.deadline < current_date, 1), else_=0)).label("expired"),
            )
            .outerjoin(TaskModel, EmployeeModel.id == TaskModel.employee_id)
            .group_by(EmployeeModel.id, EmployeeModel.surname, EmployeeModel.name, EmployeeModel.email, EmployeeModel.is_on_sick_leave, EmployeeModel.is_on_vacation)
        )
        result = self.db.execute(stmt).all()

        employees_stats = []
        for row in result:
            efficiency = (row.complete / row.count_task * 100) if row.count_task != 0 else 100.0
            employee_stat = {
                "id": row.id,
                "surname": row.surname,
                "name": row.name,
                "email": row.email,
                "count_task": row.count_task,
                "complete": row.complete,
                "expired": row.expired,
                "efficiency": f"{round(efficiency)}%",
                "is_on_sick_leave": row.is_on_sick_leave,
                "is_on_vacation": row.is_on_vacation, 
                "birth_date": None,  
            }
            employees_stats.append(employee_stat)

            efficiency_record = EmployeeEfficiencyModel(
                employee_id=row.id,
                efficiency=efficiency,
                count_task=row.count_task,
                complete=row.complete,
                expired=row.expired
            )
            self.db.add(efficiency_record)

        self.db.commit()
        return sorted(employees_stats, key=lambda x: x["id"])

    def get_employee_by_id(self, employee_id):
        current_date = date.today()
        stmt = (
            select(
                EmployeeModel.id,
                EmployeeModel.surname,
                EmployeeModel.name,
                EmployeeModel.email,
                EmployeeModel.is_on_sick_leave, 
                EmployeeModel.is_on_vacation,   
                func.count(TaskModel.id).label("count_task"),
                func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("complete"),
                func.sum(case((TaskModel.deadline < current_date, 1), else_=0)).label("expired"),
            )
            .outerjoin(TaskModel, EmployeeModel.id == TaskModel.employee_id)
            .where(EmployeeModel.id == employee_id)
            .group_by(EmployeeModel.id, EmployeeModel.surname, EmployeeModel.name, EmployeeModel.email, EmployeeModel.is_on_sick_leave, EmployeeModel.is_on_vacation)
        )
        result = self.db.execute(stmt).first()


        efficiency = (result.complete / result.count_task * 100) if result.count_task != 0 else 100.0  
        employee_stat = {
            "id": result.id,
            "surname": result.surname,
            "name": result.name,
            "email": result.email,
            "count_task": result.count_task,
            "complete": result.complete,
            "expired": result.expired,
            "efficiency": f"{round(efficiency)}%",
            "is_on_sick_leave": result.is_on_sick_leave, 
            "is_on_vacation": result.is_on_vacation,    
            "birth_date": None, 
        }

        efficiency_record = EmployeeEfficiencyModel(
            employee_id=result.id,
            efficiency=efficiency,
            count_task=result.count_task,
            complete=result.complete,
            expired=result.expired
        )
        self.db.add(efficiency_record)
        self.db.commit()

        return employee_stat

    def get_employee_by_email(self, email: str):
        return self.db.query(EmployeeModel).filter(EmployeeModel.email == email).first()

    def update_employee_password(self, employee_id: int, new_password: str):
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
        if not employee:
            return None
        employee.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.db.commit()
        return employee

    def update_employee_status(self, employee_id: int, birth_date=None, is_on_sick_leave=None, is_on_vacation=None):
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
        if not employee:
            return None
        if birth_date is not None:
            employee.birth_date = birth_date
        if is_on_sick_leave is not None:
            employee.is_on_sick_leave = is_on_sick_leave
        if is_on_vacation is not None:
            employee.is_on_vacation = is_on_vacation
        self.db.commit()
        return employee
    
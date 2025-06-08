from backend.models.EmployeeModel import EmployeeModel
from backend.models.TaskModel import TaskModel, StatusEnum
from backend.models.EmployeeEfficiencyModel import EmployeeEfficiencyModel
from sqlalchemy import select, func, case
from datetime import date, datetime
import bcrypt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            is_on_sick_leave=False,
            is_on_vacation=False
        )

        try:
            self.db.add(new_employee)
            self.db.commit()
            self.db.refresh(new_employee)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create employee: {str(e)}")
            raise
        return new_employee

    def delete_employee(self, employee_id: int):
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
        if not employee:
            return False
        self.db.delete(employee)
        self.db.commit()
        return True

    def get_all_employees(self):
        logger.info("Fetching all employees")
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
                func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("completed"),
                func.sum(case((TaskModel.deadline < current_date, 1), else_=0)).label("expired"),
            )
            .outerjoin(TaskModel, EmployeeModel.id == TaskModel.employee_id)
            .group_by(EmployeeModel.id, EmployeeModel.surname, EmployeeModel.name, EmployeeModel.email, EmployeeModel.is_on_sick_leave, EmployeeModel.is_on_vacation)
        )
        try:
            result = self.db.execute(stmt).all()
        except Exception as e:
            logger.error(f"Failed to fetch employees: {str(e)}")
            raise

        employees_stats = []
        for row in result:
            efficiency = (row.completed / row.count_task * 100) if row.count_task != 0 else 100.0
            employee_stat = {
                "id": row.id,
                "surname": row.surname,
                "name": row.name,
                "email": row.email,
                "count_task": row.count_task,
                "completed": row.completed,
                "expired": row.expired,
                "efficiency": f"{round(efficiency)}%",
                "is_on_sick_leave": row.is_on_sick_leave,
                "is_on_vacation": row.is_on_vacation,
            }
            employees_stats.append(employee_stat)

            existing_record = self.db.query(EmployeeEfficiencyModel).filter(
                EmployeeEfficiencyModel.employee_id == row.id
            ).first()
            if existing_record:
                existing_record.efficiency = efficiency
                existing_record.count_task = row.count_task
                existing_record.completed = row.completed
                existing_record.expired = row.expired
                existing_record.calculated_at = datetime.utcnow()
            else:
                efficiency_record = EmployeeEfficiencyModel(
                    employee_id=row.id,
                    efficiency=efficiency,
                    count_task=row.count_task,
                    completed=row.completed,
                    expired=row.expired,
                    calculated_at=datetime.utcnow()
                )
                self.db.add(efficiency_record)

        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to commit employee efficiency: {str(e)}")
            raise

        logger.info(f"Returning {len(employees_stats)} employees")
        return sorted(employees_stats, key=lambda x: x["id"])

    def get_employee_by_id(self, employee_id):
        logger.info(f"Fetching employee with id={employee_id}")
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
                func.sum(case((TaskModel.status == StatusEnum.выполнена, 1), else_=0)).label("completed"),
                func.sum(case((TaskModel.deadline < current_date, 1), else_=0)).label("expired"),
            )
            .outerjoin(TaskModel, EmployeeModel.id == TaskModel.employee_id)
            .where(EmployeeModel.id == employee_id)
            .group_by(EmployeeModel.id, EmployeeModel.surname, EmployeeModel.name, EmployeeModel.email, EmployeeModel.is_on_sick_leave, EmployeeModel.is_on_vacation)
        )
        try:
            result = self.db.execute(stmt).first()
        except Exception as e:
            logger.error(f"Failed to fetch employee {employee_id}: {str(e)}")
            raise

        efficiency = (result.completed / result.count_task * 100) if result.count_task != 0 else 100.0
        employee_stat = {
            "id": result.id,
            "surname": result.surname,
            "name": result.name,
            "email": result.email,
            "count_task": result.count_task,
            "completed": result.completed,
            "expired": result.expired,
            "efficiency": f"{round(efficiency)}%",
            "is_on_sick_leave": result.is_on_sick_leave,
            "is_on_vacation": result.is_on_vacation,
        }

        existing_record = self.db.query(EmployeeEfficiencyModel).filter(
            EmployeeEfficiencyModel.employee_id == result.id
        ).first()
        if existing_record:
            existing_record.efficiency = efficiency
            existing_record.count_task = result.count_task
            existing_record.completed = result.completed
            existing_record.expired = result.expired
            existing_record.calculated_at = datetime.utcnow()
        else:
            efficiency_record = EmployeeEfficiencyModel(
                employee_id=result.id,
                efficiency=efficiency,
                count_task=result.count_task,
                completed=result.completed,
                expired=result.expired,
                calculated_at=datetime.utcnow()
            )
            self.db.add(efficiency_record)

        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to commit employee efficiency: {str(e)}")
            raise

        return employee_stat

    def get_employee_by_email(self, email: str):
        try:
            return self.db.query(EmployeeModel).filter(EmployeeModel.email == email).first()
        except Exception as e:
            logger.error(f"Failed to fetch employee by email {email}: {str(e)}")
            raise

    def update_employee_password(self, employee_id: int, new_password: str):
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
        if not employee:
            return None
        employee.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update password for employee {employee_id}: {str(e)}")
            raise
        return employee

    def update_employee_status(self, employee_id: int, is_on_sick_leave=None, is_on_vacation=None):
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
        if not employee:
            return None
        if is_on_sick_leave is not None:
            employee.is_on_sick_leave = is_on_sick_leave
        if is_on_vacation is not None:
            employee.is_on_vacation = is_on_vacation
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update status for employee {employee_id}: {str(e)}")
            raise
        return employee
    
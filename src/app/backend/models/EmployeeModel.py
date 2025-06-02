import enum
from backend.utlis.db import Base
from sqlalchemy import Column, Integer, String, Enum, Date, Boolean

class RoleEnum(str, enum.Enum):
    руководитель = "руководитель"
    исполнитель = "исполнитель"

class EmployeeModel(Base):
    __tablename__ = "Employee"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String(40), nullable=False)
    name = Column(String(30), nullable=False)
    lastname = Column(String(40))
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    birth_date = Column(Date, nullable=True)
    is_on_sick_leave = Column(Boolean, nullable=False, default=False)
    is_on_vacation = Column(Boolean, nullable=False, default=False)
    
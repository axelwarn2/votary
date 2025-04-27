from sqlalchemy import Column, Integer, String, Enum
from backend.utlis.db import Base
import enum

class RoleEnum(str, enum.Enum):
    руководитель = "руководитель"
    исполнитель = "исполнитель"

class Employee(Base):
    __tablename__ = "Employee"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String(40), nullable=False)
    name = Column(String(30), nullable=False)
    lastname = Column(String(40))
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

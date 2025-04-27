# backend/schemas/employee.py
from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    surname: str
    name: str
    lastname: str
    email: str
    password: str
    role: str

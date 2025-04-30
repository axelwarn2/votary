# backend/schemas/employee.py
from pydantic import BaseModel
from typing import Optional

class EmployeeCreate(BaseModel):
    id: int
    surname: str
    name: str
    lastname: str
    email: str
    password: str
    role: str

class EmployeeRead(BaseModel):
    id: int
    surname: str
    name: str
    lastname: Optional[str] = None
    email: str
    password: str
    role: str

    class Config:
        orm_mode = True

class EmployeeStats(BaseModel):
    id: int
    surname: str
    name: str
    count_task: int
    complete: int
    expired: int
    efficiency: str

    class Config:
        orm_mode = True
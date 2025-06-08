from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmployeeCreate(BaseModel):
    surname: str
    name: str
    lastname: str
    email: str
    password: str
    role: str
    is_on_sick_leave: Optional[bool] = False
    is_on_vacation: Optional[bool] = False

class EmployeeStats(BaseModel):
    id: int
    surname: str
    name: str
    email: str
    count_task: int
    completed: int  # Исправлено с complete на completed
    expired: int
    efficiency: str
    is_on_sick_leave: Optional[bool] = False
    is_on_vacation: Optional[bool] = False

    class Config:
        from_attributes = True  # Обновлено для Pydantic v2

class EmployeeRead(BaseModel):
    id: int
    surname: str
    name: str
    lastname: Optional[str]
    email: str
    count_task: int
    completed: int  # Исправлено с complete на completed
    expired: int
    efficiency: str
    is_on_sick_leave: Optional[bool] = False
    is_on_vacation: Optional[bool] = False

    class Config:
        orm_mode = True

class EmployeeLogin(BaseModel):
    email: str
    password: str

class PasswordResetRequest(BaseModel):
    email: str
    password: str
    password_confirm: str

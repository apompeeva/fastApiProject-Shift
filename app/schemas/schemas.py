from pydantic import BaseModel, EmailStr
from datetime import date
from fastapi_users import schemas, models
from typing import Optional


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    login: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    login: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class SalaryData(BaseModel):
    current_salary: int
    increase_date: date


class SalaryDataCreate(SalaryData):
    user_id: int



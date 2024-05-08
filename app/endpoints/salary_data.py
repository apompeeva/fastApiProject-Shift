from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import current_user, current_superuser
from app.crud.crud import create_salary_data, get_current_user_salary_data
from app.database import get_async_session
from app.models.models import User
from app.schemas.schemas import SalaryDataCreate

salary_router = APIRouter()


@salary_router.post("/salary_data", dependencies=[Depends(current_superuser)])
async def create_new_salary_data(salary_data: SalaryDataCreate,
                                session: AsyncSession = Depends(get_async_session)):
    new_salary_info = await create_salary_data(salary_data, session)
    return new_salary_info


@salary_router.get("/salary_data")
async def get_salary_data(session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)):

    salary_info = await get_current_user_salary_data(user, session)
    return salary_info

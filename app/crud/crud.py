from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User, SalaryData
from app.schemas.schemas import SalaryDataCreate


async def create_salary_data(new_salary_info: SalaryDataCreate, session: AsyncSession) -> SalaryData:
    new_salary_info_data = new_salary_info.dict()
    db_salary_info = SalaryData(**new_salary_info_data)
    session.add(db_salary_info)
    await session.commit()
    await session.refresh(db_salary_info)
    return db_salary_info


async def get_current_user_salary_data(user: User, session: AsyncSession):
    salary_info = await session.execute(select(SalaryData).where(SalaryData.user_id == user.id))
    salary_info = salary_info.scalars().first()
    return salary_info

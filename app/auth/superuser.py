import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from app.auth.manager import get_user_db, get_user_manager
from app.database import get_async_session
from app.schemas.schemas import UserCreate
from config import FIRST_SUPERUSER_EMAIL, FIRST_SUPERUSER_PASSWORD

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False, login: str = "login"):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(email=email, password=password, is_superuser=is_superuser, login=login)
                    )
                    print(f"User created {user}")
                    return user
    except UserAlreadyExists:
        pass


async def create_superuser():
    await create_user(email=FIRST_SUPERUSER_EMAIL, password=FIRST_SUPERUSER_PASSWORD, is_superuser=True)

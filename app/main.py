from fastapi import FastAPI

from app.auth.auth import auth_backend
from app.auth.manager import fastapi_users
from app.auth.superuser import create_superuser
from app.endpoints.salary_data import salary_router

from app.schemas.schemas import UserRead, UserCreate


app = FastAPI()

app.include_router(salary_router, tags=["salary"])

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.on_event('startup')
async def startup():
    await create_superuser()






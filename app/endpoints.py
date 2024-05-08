from fastapi import APIRouter, Depends
from fastapi_users import fastapi_users

from app.auth.database import User

router = APIRouter()

fake_users = {
    1: {"login": "john_doe", "password": "john@example.com"},
    2: {"login": "jane_smith", "password": "jane@example.com"},
}


@router.get("/users/")
def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


# Конечная точка для получения информации о пользователе по ID
@router.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}



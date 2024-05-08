import json
import time

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.models.models import User
from tests.conftest import async_session_maker

"""
TO DO:
- вынести параметры в отдельный файл
- добавить тест кейсы для кодов 400 и 422
- дописать тесткейсы для добавления и простмотра зрплаты
"""

superuser_registration_data = [{
        "email": "superuser@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "login": "superuser"
    }]

superuser_signin_data= [{
        "username": "superuser@example.com",
        "password": "string",
    }]

user_registration_data = [{
        "login": "testuser1",
        "email": "testuser1@example.com",
        "password": "test1",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    }]

user_signin_data = [{
            "username": "testuser1@example.com",
            "password": "test1"
        }]
superuser_token = ""
users_tokens = {}


def get_cookies(set_cookie_header: str) -> httpx.Cookies:
    cookies = httpx.Cookies()
    entries = set_cookie_header.split(", ")
    for entry in entries:
        chunks = entry.split("; ")
        chunk = next(c for c in chunks)
        k, v = chunk.split("=")
        cookies.set(k, v)
    return cookies


@pytest.mark.parametrize("superuser_json", superuser_registration_data)
async def test_register_superuser(ac: AsyncClient, superuser_json):
    """Регистрация и авторизация суперпользователя."""
    response = await ac.post('/auth/register', json=superuser_json)
    assert response.status_code == 201

    async with async_session_maker() as session:
        superuser = await session.execute(select(User))
        superuser = superuser.scalars().first()
        superuser.is_superuser = True
        await session.commit()


@pytest.mark.parametrize("superuser_json", superuser_signin_data)
async def test_signin_superuser(ac: AsyncClient, superuser_json):
    response = await ac.post(
        '/auth/jwt/login',
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=superuser_json)
    cookies = get_cookies(response.headers["set-cookie"])
    global superuser_token
    superuser_token = cookies.get("fastapiusersauth")
    assert response.status_code == 204
    assert cookies is not None


@pytest.mark.parametrize("user_json", user_registration_data)
async def test_register_testuser(ac: AsyncClient, user_json):
    """Регистрация и авторизация тестового пользователя - testuser1."""
    response = await ac.post('/auth/register', json=user_json)
    # global testuser1_id
    # testuser1_id = json.loads(response.text)['id']
    assert response.status_code == 201


@pytest.mark.parametrize("user_json", user_signin_data)
async def test_signin_testuser(ac: AsyncClient, user_json):
    response = await ac.post(
        '/auth/jwt/login',
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=user_json)

    global user_token
    cookies = get_cookies(response.headers["set-cookie"])
    user_token = cookies.get("fastapiusersauth")
    assert response.status_code == 204
    assert cookies is not None

#
# async def test_salary_info_create(ac: AsyncClient):
#     """Создание суперпользователем записей о зарплате для testuser1 и testuser2."""
#     salary_info_for_testuser1 = {
#         "current_salary": 50000,
#         "salary_increase_date": '2023-10-15',
#         "user_id": f"{testuser1_id}"
#     }
#
#     salary_info_for_testuser2 = {
#         "current_salary": 100000,
#         "salary_increase_date": "2023-12-31",
#         "user_id": f"{testuser2_id}"
#     }
#
#     response = await ac.post(
#         '/salary_info',
#         headers={'Authorization': f'Bearer {superuser_token}'},
#         json=salary_info_for_testuser1
#     )
#
#     assert {"current_salary":50000,"salary_increase_date":"2023-10-15"} == json.loads(response.text)
#
#     response = await ac.post(
#         '/salary_info',
#         headers={'Authorization': f'Bearer {superuser_token}'},
#         json=salary_info_for_testuser2
#     )
#
#     assert {"current_salary":100000,"salary_increase_date":"2023-12-31"} == json.loads(response.text)
#
#
# async def test_testuser1_get_own_salary_info(ac: AsyncClient):
#     """Получение testuser1 своей информации о зарплате (с использованием токена)."""
#     response = await ac.get(
#         '/salary_info',
#         headers={'Authorization': f'Bearer {testuser1_token}'},
#     )
#
#     assert {"current_salary": 50000, "salary_increase_date": "2023-10-15"} == json.loads(response.text)
#
#
# async def test_testuser2_get_own_salary_info(ac: AsyncClient):
#     """Получение testuser2 своей информации о зарплате (с использованием токена)."""
#     response = await ac.get(
#         '/salary_info',
#         headers={'Authorization': f'Bearer {testuser2_token}'},
#     )
#
#     assert {"current_salary":100000,"salary_increase_date":"2023-12-31"} == json.loads(response.text)
#
#
# async def test_get_salary_info_without_token(ac: AsyncClient):
#     """Получение информации о зарплате без токена"""
#     response = await ac.get(
#         '/salary_info',
#     )
#
#     assert response.status_code == 401
#
#
# async def test_get_testuser1_salary_info_with_expired_token(ac: AsyncClient):
#     """Получение testuser1 информации о своей зарплате с использованием токена с истекшим сроком."""
#     settings.jwt_lifetime_seconds = 1
#     response = await ac.post(
#         '/auth/jwt/login',
#         headers={"Content-Type": "application/x-www-form-urlencoded"},
#         data={
#             "username": "testuser1@example.com",
#             "password": "test1"
#         })
#
#     global testuser1_token
#     testuser1_token = json.loads(response.text)['access_token']
#
#     response = await ac.get(
#         '/salary_info',
#         headers={'Authorization': f'Bearer {testuser1_token}'},
#     )
#
#     assert {"current_salary": 50000, "salary_increase_date": "2023-10-15"} == json.loads(response.text)
#
#     time.sleep(2)
#
#     response = await ac.get(
#         '/salary_info',
#         headers={'Authorization': f'Bearer {testuser1_token}'},
#     )
#
#     assert response.status_code == 401

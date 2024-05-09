import pytest
from httpx import AsyncClient
from sqlalchemy import select

from models.models import User
from config import FIRST_SUPERUSER_EMAIL, FIRST_SUPERUSER_PASSWORD
from tests.conftest import async_session_maker
from tests.params import user_registration_data, user_signin_data, salary_info

import json


class TestGetSalaryData:
    @pytest.mark.parametrize("salary_info, user_json", list(zip(salary_info, user_registration_data)))
    async def test_salary_info_create(self, ac: AsyncClient, setup, salary_info, user_json):
        """Создание суперпользователем записей о зарплате для testuser."""

        superuser_json = {"username": FIRST_SUPERUSER_EMAIL, "password": FIRST_SUPERUSER_PASSWORD}

        response = await ac.post("/auth/register", json=user_json)
        assert response.status_code == 201
        id = json.loads(response.text)["id"]

        response = await ac.post(
            "/auth/jwt/login", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=superuser_json
        )
        # cookies = get_cookies(response.headers["set-cookie"])
        # superuser_token = cookies.get("fastapiusersauth")
        assert response.status_code == 204

        user_salary_info = salary_info
        user_salary_info["user_id"] = id

        response = await ac.post(
            "/salary_data",
            json=user_salary_info,
        )
        assert response.status_code == 200
        assert salary_info["current_salary"] == json.loads(response.text)["current_salary"]
        assert salary_info["increase_date"] == json.loads(response.text)["increase_date"]

    @pytest.fixture(scope="class")
    async def setup(self, ac):
        superuser_registration_data = {
            "email": FIRST_SUPERUSER_EMAIL,
            "password": FIRST_SUPERUSER_PASSWORD,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "login": "superuser",
        }

        response = await ac.post("/auth/register", json=superuser_registration_data)
        assert response.status_code == 201

        async with async_session_maker() as session:
            superuser = await session.execute(select(User))
            superuser = superuser.scalars().first()
            superuser.is_superuser = True
            await session.commit()

    @pytest.mark.parametrize("user_json", user_signin_data)
    async def test_testuser_get_own_salary_info(self, ac: AsyncClient, user_json):
        """Получение testuser своей информации о зарплате (с использованием токена)."""
        response = await ac.post(
            "/auth/jwt/login", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=user_json
        )
        assert response.status_code == 204

        response = await ac.get(
            "/salary_data",
        )

        assert response.status_code == 200

    async def test_get_salary_info_without_token(self, ac: AsyncClient):
        """Получение информации о зарплате без токена"""
        await ac.post(
            "/auth/jwt/logout",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response = await ac.get("/salary_data", cookies=None)

        assert response.status_code == 401

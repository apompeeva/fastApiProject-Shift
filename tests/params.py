superuser_registration_data = [
    {
        "email": "superuser@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "login": "superuser",
    }
]

superuser_signin_data = [
    {
        "username": "superuser@example.com",
        "password": "string",
    }
]

user_registration_data = [
    {
        "login": "testuser1",
        "email": "testuser1@example.com",
        "password": "test1",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    },
    {
        "login": "testuser2",
        "email": "testuser2@example.com",
        "password": "test2",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    },
]

user_signin_data = [
    {"username": "testuser1@example.com", "password": "test1"},
    {"username": "testuser1@example.com", "password": "test1"},
]

salary_info = [
    {"current_salary": 50000, "increase_date": "2023-10-15T00:00:00"},
    {"current_salary": 100000, "increase_date": "2023-12-31T00:00:00"},
]

# Salary

## Техническое заданиие 
Реализуйте REST-сервис просмотра текущей зарплаты и даты следующего
повышения. Из-за того, что такие данные очень важны и критичны, каждый
сотрудник может видеть только свою сумму. Для обеспечения безопасности, вам
потребуется реализовать метод где по логину и паролю сотрудника будет выдан
секретный токен, который действует в течение определенного времени. Запрос
данных о зарплате должен выдаваться только при предъявлении валидного токена.

## Необязательные технические требования
- зависимости зафиксированы менеджером зависимостей **poetry**
- написаны тесты с использованием **pytest**
- реализована возможность собирать и запускать контейнер с сервисом в **Docker**

## Стек
- Python
- FastAPI
- PostgreSQL
- fastapi-users
- Sqlalchemy
- Uvicorn
- Alembic
- Poetry
- pytest-asyncio
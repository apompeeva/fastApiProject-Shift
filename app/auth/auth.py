from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from config import EXPIRATION_TIME, SECRET

cookie_transport = CookieTransport(cookie_max_age=EXPIRATION_TIME)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=EXPIRATION_TIME)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
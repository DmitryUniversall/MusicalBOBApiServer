from src.app.core import BaseSchema


class AuthTokenPair(BaseSchema):
    access_token: str
    refresh_token: str

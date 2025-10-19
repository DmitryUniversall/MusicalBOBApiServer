from src.app.core import BaseSchema
from .auth_session import AuthSessionInternal
from src.app.main.components.users import UserInternal


class AuthInfo(BaseSchema):
    user: UserInternal
    session: AuthSessionInternal

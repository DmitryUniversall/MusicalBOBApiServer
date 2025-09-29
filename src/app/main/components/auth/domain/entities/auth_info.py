from src.app.core import BaseSchema
from src.app.main.components.auth.domain import AuthSessionInternal
from src.app.main.components.users.domain import UserInternal


class AuthInfo(BaseSchema):
    user: UserInternal
    session: AuthSessionInternal

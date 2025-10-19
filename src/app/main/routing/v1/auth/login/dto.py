from pydantic import Field

from src.app.core import BaseSchema
from src.app.main.components.auth import AuthSessionPrivate
from src.app.main.components.users import UserPrivate


class LoginRequestDTO(BaseSchema):
    username: str
    session_name: str
    password: str = Field(..., max_length=50)


class LoginResponseDTO(BaseSchema):
    user: UserPrivate
    session: AuthSessionPrivate
    access_token: str  # TODO: Use AuthTokenPair?
    refresh_token: str

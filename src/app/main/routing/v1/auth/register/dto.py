from pydantic import Field

from src.app.core import BaseSchema
from src.app.main.components.auth import AuthSessionPrivate
from src.app.main.components.users import UserPrivate


class RegisterRequestDTO(BaseSchema):
    username: str
    session_name: str
    password: str = Field(..., max_length=50)


class RegisterResponseDTO(BaseSchema):
    user: UserPrivate
    session: AuthSessionPrivate
    access_token: str
    refresh_token: str

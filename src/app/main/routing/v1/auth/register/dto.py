from pydantic import Field

from app.core import BaseSchema
from app.main.components.auth import AuthSessionPrivate
from app.main.components.users import UserPrivate


class RegisterRequestDTO(BaseSchema):
    username: str
    session_name: str
    password: str = Field(..., max_length=50)


class RegisterResponseDTO(BaseSchema):
    user: UserPrivate
    session: AuthSessionPrivate
    access_token: str  # TODO: Use AuthTokenPair?
    refresh_token: str

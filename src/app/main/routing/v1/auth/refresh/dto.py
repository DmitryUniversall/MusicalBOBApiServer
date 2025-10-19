from pydantic import Field

from src.app.core import BaseSchema


class RefreshRequestDTO(BaseSchema):
    refresh_token: str = Field(..., max_length=1000)


class RefreshResponseDTO(BaseSchema):
    access_token: str
    refresh_token: str

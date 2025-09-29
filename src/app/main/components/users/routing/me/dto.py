from src.app.core import BaseSchema
from src.app.main.components.users.domain import UserPrivate


class GetMeResponseDTO(BaseSchema):
    user: UserPrivate

from uuid import uuid4

from pydantic import Field

from src.app.core import BaseSchema
from src.base.utils.types import UUIDString


class ExternalObject(BaseSchema):
    uuid: UUIDString = Field(default_factory=lambda: str(uuid4()))
    source: str

from typing import Optional, Any
from uuid import uuid4

from pydantic import Field

from src.app.core import BaseSchema
from src.base.utils.types import UUIDString
from .search_platform import SearchPlatform


class SearchEntity(BaseSchema):
    uuid: UUIDString = Field(default_factory=lambda: str(uuid4()))
    title: str
    source: str
    platform: SearchPlatform
    image_source: Optional[str]

    raw: Optional[Any] = Field(default=None, exclude=True)

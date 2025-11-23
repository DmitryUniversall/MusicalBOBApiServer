from typing import Optional, Any

from pydantic import Field

from src.app.main.common.entities import ExternalObject
from .search_platform import SearchPlatform


class SearchEntity(ExternalObject):
    title: str
    platform: SearchPlatform
    image_source: Optional[str]

    raw: Optional[Any] = Field(default=None, exclude=True)

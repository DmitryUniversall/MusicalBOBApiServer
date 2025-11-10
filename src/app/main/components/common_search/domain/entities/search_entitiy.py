from typing import Optional, Any

from pydantic import Field

from src.app.core import BaseSchema
from .search_platform import SearchPlatform


class BaseSearchEntity(BaseSchema):
    title: str
    source: str
    platform: SearchPlatform
    image_source: Optional[str]

    raw: Optional[Any] = Field(default=None, exclude=True)

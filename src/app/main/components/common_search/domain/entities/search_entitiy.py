from typing import Optional

from src.app.core import BaseSchema
from .search_platform import SearchPlatform


class BaseSearchEntity(BaseSchema):
    title: str
    source: str
    platform: SearchPlatform
    image_source: Optional[str]

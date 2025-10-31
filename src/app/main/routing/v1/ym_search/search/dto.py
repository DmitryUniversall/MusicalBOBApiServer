from pydantic import Field

from src.app.core import BaseSchema
from src.app.main.components.common_search import MediaContent, MediaContentType


class SearchResultDTO(BaseSchema):
    type_: MediaContentType = Field(alias="type")
    media: MediaContent

from pydantic import Field

from src.app.core import BaseSchema
from src.app.main.components.common_search import MediaContent, MediaContentType, Playlist, Track


class SearchResultDTO[T: MediaContent](BaseSchema):
    type_: MediaContentType = Field(alias="type")
    media: Track | Playlist


SearchResultDTO.model_rebuild()

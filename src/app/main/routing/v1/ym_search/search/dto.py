from pydantic import Field, ConfigDict

from src.app.core import BaseSchema
from src.app.main.components.common_search import MediaContentType, Playlist, Track


class SearchResultDTO(BaseSchema):
    type_: MediaContentType = Field(alias="type", serialization_alias="type")
    media: Track | Playlist

    model_config = ConfigDict(serialize_by_alias=True)


SearchResultDTO.model_rebuild()

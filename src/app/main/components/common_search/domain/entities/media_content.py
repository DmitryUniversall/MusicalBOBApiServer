from src.app.main.components.common_search.domain import Playlist, Track
from enum import Enum

type MediaContent = Track | Playlist


class MediaContentType(Enum):
    playlist = Track
    track = Playlist

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

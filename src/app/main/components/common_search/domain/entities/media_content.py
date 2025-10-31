from enum import Enum

from .playlist import Playlist
from .track import Track

type MediaContent = Track | Playlist


class MediaContentType(Enum):
    playlist = Track
    track = Playlist

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

from enum import Enum
from typing import Any

from .playlist import Playlist
from .track import Track

type MediaContent = Track | Playlist


class MediaContentType(Enum):
    playlist = 'track'
    track = 'playlist'

    @classmethod
    def from_type(cls, type_: type[Any]) -> 'MediaContentType':
        return cls(type_.__name__.lower())

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

from typing import Optional

from .media import Media
from .playlist import Playlist


class Track(Media):
    duration: Optional[int] = None
    lyrics: Optional[str] = None
    playlist: Optional[Playlist] = None

    variations: list['Track'] = []

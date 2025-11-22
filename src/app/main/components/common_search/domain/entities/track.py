from typing import Optional

from .lyrics import Lyrics
from .media import Media
from .playlist import Playlist


class Track(Media):
    duration: Optional[int] = None
    lyrics: Optional[Lyrics] = None
    playlist: Optional[Playlist] = None

    variations: list['Track'] = []


Playlist.model_rebuild()

from typing import Optional

from .audio_sources import AudioSource
from .media import Media
from .playlist import Playlist


class Track(Media):
    duration: Optional[int]
    lyrics: Optional[str]
    playlist: Optional[Playlist]
    audio_sources: Optional[list[AudioSource]]
    variations: list['Track'] = []

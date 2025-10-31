from typing import Optional

from .audio_sources import AudioSource
from .media import Media
from .playlist import Playlist


class Track(Media):
    audio_sources: list[AudioSource] = []
    variations: list['Track'] = []

    duration: Optional[int] = None
    lyrics: Optional[str] = None
    playlist: Optional[Playlist] = None

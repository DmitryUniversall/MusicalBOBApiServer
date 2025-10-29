from typing import TYPE_CHECKING, Iterable

from .media import Media

if TYPE_CHECKING:
    from .track import Track


class Playlist(Media):
    tracks: list['Track'] = []

    def extend(self, tracks: Iterable['Track']) -> None:
        self.tracks.extend(tracks)

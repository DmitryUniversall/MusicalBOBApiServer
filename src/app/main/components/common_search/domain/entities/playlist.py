from typing import TYPE_CHECKING, Iterable

from pydantic import Field

from .media import Media

if TYPE_CHECKING:
    from .track import Track


class Playlist(Media):
    tracks: list['Track'] = Field(default_factory=list)

    def extend(self, tracks: Iterable['Track']) -> None:
        self.tracks.extend(tracks)

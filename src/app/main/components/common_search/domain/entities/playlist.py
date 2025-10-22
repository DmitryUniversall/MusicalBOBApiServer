from typing import TYPE_CHECKING

from src.app.main.components.search.entities.media import Media

if TYPE_CHECKING:
    from .track import Track


class Playlist(Media):
    tracks: list['Track'] = []

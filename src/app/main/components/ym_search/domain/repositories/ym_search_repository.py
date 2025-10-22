from abc import ABC, abstractmethod

from src.app.main.components.common_search import Playlist, Track
from src.base.utils.interface import InterfaceMeta


class YMSearchRepositoryI(ABC, metaclass=InterfaceMeta):
    @abstractmethod
    async def get_album_by_url(self, url: str) -> Playlist:
        ...

    @abstractmethod
    async def get_playlist_by_url(self, url: str) -> Playlist:
        ...

    @abstractmethod
    async def get_track_by_url(self, url: str) -> Track:
        ...

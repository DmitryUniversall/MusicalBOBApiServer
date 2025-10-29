from abc import ABC
from typing import Optional

from src.app.main.components.common_search import MediaContent, AudioSource
from src.app.main.components.common_search.domain.services import AbstractPlatformSearchService
from src.base.utils.interface import InterfaceMeta


class YMSearchServiceI(AbstractPlatformSearchService, ABC, metaclass=InterfaceMeta):
    async def search_by_url(self, url: str) -> MediaContent:
        ...

    async def search_by_name(self, query: str) -> MediaContent:
        ...

    async def get_audio_sources(self, url: str) -> tuple[AudioSource, ...]:
        ...

    async def get_lyrics(self, url: str) -> Optional[str]:
        ...

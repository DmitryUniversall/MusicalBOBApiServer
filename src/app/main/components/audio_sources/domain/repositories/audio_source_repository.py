from abc import ABC, abstractmethod
from typing import Optional, Iterable

from src.base.utils.types import UUIDString
from ..entities import AudioSource


class AudioSourceRepositoryI(ABC):
    @abstractmethod
    async def cache_audio_source(self, audio_source: AudioSource) -> None:
        ...

    @abstractmethod
    async def cache_audio_sources(self, audio_sources: Iterable[AudioSource]) -> None:
        ...

    @abstractmethod
    async def get_cached_audio_source(self, uuid: UUIDString) -> Optional[AudioSource]:
        ...

    @abstractmethod
    async def cache_audio_source_and_map_with_track(self, track_source: str, audio_source: AudioSource) -> None:
        ...

    @abstractmethod
    async def cache_audio_sources_and_map_with_track(self, track_source: str, audio_sources: Iterable[AudioSource]) -> None:
        ...

    @abstractmethod
    async def get_cached_audio_sources_for_track(self, track_source: str) -> tuple[AudioSource, ...]:
        ...

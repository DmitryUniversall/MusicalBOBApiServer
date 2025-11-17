from abc import ABC, abstractmethod
from typing import Optional, Iterable

from src.app.main.components.audio_sources.domain import AudioSource
from src.base.utils.types import UUIDString


class AudioSourceServiceI(ABC):
    @abstractmethod
    async def get_cached_audio_source(self, uuid: UUIDString) -> Optional[AudioSource]:
        ...

    @abstractmethod
    async def cache_audio_source(self, audio_source: AudioSource) -> None:
        ...

    @abstractmethod
    async def cache_audio_sources(self, audio_source: Iterable[AudioSource]) -> None:
        ...

    @abstractmethod
    async def get_cached_audio_sources_for_track(self, track_uuid: UUIDString) -> tuple[AudioSource, ...]:
        ...

    @abstractmethod
    async def cache_audio_source_for_track(self, track_uuid: UUIDString, audio_source: AudioSource) -> None:
        ...

    @abstractmethod
    async def cache_audio_sources_for_track(self, track_uuid: UUIDString, audio_sources: Iterable[AudioSource]) -> None:
        ...

from typing import Optional, Iterable

from src.app.main.components.audio_sources.domain import AudioSourceServiceI, AudioSource, AudioSourceRepositoryI
from src.base.utils.types import UUIDString


class AudioSourceServiceImpl(AudioSourceServiceI):
    def __init__(self, _audio_source_repository: AudioSourceRepositoryI) -> None:
        self._audio_source_repository = _audio_source_repository

    async def cache_audio_source(self, audio_source: AudioSource) -> None:
        await self._audio_source_repository.cache_audio_source(audio_source)

    async def cache_audio_sources(self, audio_sources: Iterable[AudioSource]) -> None:
        await self._audio_source_repository.cache_audio_sources(audio_sources)

    async def get_cached_audio_source(self, uuid: UUIDString) -> Optional[AudioSource]:
        return await self._audio_source_repository.get_cached_audio_source(uuid)

    async def cache_audio_source_and_map_with_track(self, track_source: str, audio_source: AudioSource) -> None:
        await self._audio_source_repository.cache_audio_source_and_map_with_track(track_source, audio_source)

    async def cache_audio_sources_and_map_with_track(self, track_source: str, audio_sources: Iterable[AudioSource]) -> None:
        await self._audio_source_repository.cache_audio_sources_and_map_with_track(track_source, audio_sources)

    async def get_cached_audio_sources_for_track(self, track_source: str) -> tuple[AudioSource, ...]:
        return tuple(await self._audio_source_repository.get_cached_audio_sources_for_track(track_source))

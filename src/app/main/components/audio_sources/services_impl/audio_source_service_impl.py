from typing import Optional, Iterable

from src.app.main.components.audio_sources.domain import AudioSourceServiceI, AudioSource, AudioSourceRepositoryI
from src.base.state import project_settings
from src.base.utils.types import UUIDString


class AudioSourceServiceImpl(AudioSourceServiceI):
    _CACHED_AUDIO_SOURCE_PATH: str = f"http://{project_settings.HOST}:{project_settings.PORT}/v1/audio_sources"

    def __init__(self, _audio_source_repository: AudioSourceRepositoryI) -> None:
        self._audio_source_repository = _audio_source_repository

    def _get_cached_audio_source_url(self, uuid: UUIDString) -> str:
        return f"{self._CACHED_AUDIO_SOURCE_PATH}/{uuid}/"

    async def cache_audio_source_for_track(self, track_uuid: UUIDString, audio_source: AudioSource) -> None:
        await self._audio_source_repository.cache_audio_source_for_track(track_uuid, audio_source)

    async def cache_audio_sources_for_track(self, track_uuid: UUIDString, audio_sources: Iterable[AudioSource]) -> None:
        await self._audio_source_repository.cache_audio_sources_for_track(track_uuid, audio_sources)

    async def get_cached_audio_source(self, uuid: UUIDString) -> Optional[AudioSource]:
        return await self._audio_source_repository.get_cached_audio_source(uuid)

    async def cache_audio_source(self, audio_source: AudioSource) -> None:
        await self._audio_source_repository.cache_audio_source(audio_source)

    async def cache_audio_sources(self, audio_sources: Iterable[AudioSource]) -> None:
        await self._audio_source_repository.cache_audio_sources(audio_sources)

    async def get_cached_audio_sources_for_track(self, track_uuid: UUIDString) -> tuple[AudioSource, ...]:
        return tuple(
            await self._audio_source_repository.get_cached_audio_sources_for_track(track_uuid)
        )

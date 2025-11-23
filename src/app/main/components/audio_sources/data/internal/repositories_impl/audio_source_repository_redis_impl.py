import logging
from datetime import datetime
from typing import Optional, Iterable

from redis import asyncio as aioredis

from src.app.main.common.redis import RedisCache
from src.app.main.common.redis.collections.redis_hset import RedisHSet
from src.app.main.components.audio_sources.domain import AudioSourceRepositoryI, AudioSource
from src.base.state import project_settings
from src.base.utils.async_tools import gather_all
from src.base.utils.types import UUIDString

_logger = logging.getLogger(__name__)


class AudioSourceRepositoryRedisImpl(AudioSourceRepositoryI):
    def __init__(self, redis_client: aioredis.client.Redis) -> None:
        self._redis_client = redis_client

        self._cache = RedisCache(
            redis_client=self._redis_client,
            key=project_settings.AUDIO_SOURCE_CACHE_REDIS_KEY,
            max_size=project_settings.AUDIO_SOURCE_CACHE_MAX_SIZE
        )

    def _get_track_audio_sources_key(self, track_source: str) -> str:
        return f"{project_settings.AUDIO_SOURCES_FOR_TRACK_REDIS_KEY}:{track_source}"

    async def _get_track_audio_sources_hset(self, track_source: str) -> RedisHSet:
        key = self._get_track_audio_sources_key(track_source)

        return RedisHSet(
            key=key,
            redis_client=self._redis_client,
            max_size=project_settings.AUDIO_SOURCE_CACHE_MAX_SIZE
        )

    async def _get_audio_source_uuids_for_track(self, track_source: str) -> list[UUIDString]:
        hset = await self._get_track_audio_sources_hset(track_source)
        keys = await hset.get_keys()

        expired = []
        sources = []
        for timestamp in keys:
            if datetime.fromtimestamp(float(timestamp)) < datetime.now():
                expired.append(timestamp)
                continue

            if (cached := await hset.read_data(timestamp)) is None:
                _logger.error("Unable to get audio source from cache; Redis db might be changed externally")
                continue

            sources.append(cached)

        if expired:
            await hset.delete(*expired)

        return sources

    async def _cache_audio_source_and_map_with_track(self, source: AudioSource, track_audio_sources_hset: RedisHSet) -> None:
        await self.cache_audio_source(source)
        await track_audio_sources_hset.write_data(str(source.expires_at.timestamp()), source.uuid)

    async def cache_audio_source(self, audio_source: AudioSource) -> None:
        await self._cache.write_schema(audio_source.uuid, audio_source)

    async def cache_audio_sources(self, audio_sources: Iterable[AudioSource]) -> None:
        await gather_all(self._cache.write_schema(audio_source.uuid, audio_source) for audio_source in audio_sources)

    async def get_cached_audio_source(self, uuid: UUIDString) -> Optional[AudioSource]:
        return await self._cache.read_schema(uuid, schema_cls=AudioSource)

    async def cache_audio_source_and_map_with_track(self, track_source: str, audio_source: AudioSource) -> None:
        hset = await self._get_track_audio_sources_hset(track_source)
        await self._cache_audio_source_and_map_with_track(audio_source, hset)

    async def cache_audio_sources_and_map_with_track(self, track_source: str, audio_sources: Iterable[AudioSource]) -> None:
        hset = await self._get_track_audio_sources_hset(track_source)
        await gather_all((self._cache_audio_source_and_map_with_track(source, hset) for source in audio_sources))

    async def get_cached_audio_sources_for_track(self, track_source: str) -> tuple[AudioSource, ...]:
        uuids = await self._get_audio_source_uuids_for_track(track_source)

        sources = []
        for uuid in uuids:
            if (cached := await self.get_cached_audio_source(uuid)) is None:
                _logger.warning(f"Skipping expired audio source '{uuid}' for track {track_source}")
                continue

            sources.append(cached)

        return tuple(sources)

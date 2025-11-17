from datetime import datetime
from typing import Optional, Iterable

from redis import asyncio as aioredis

from src.app.main.common.redis import RedisCache
from src.app.main.common.redis.collections.redis_hset import RedisHSet
from src.app.main.components.audio_sources.domain import AudioSourceRepositoryI, AudioSource
from src.base.state import project_settings
from src.base.utils.async_tools import gather_all
from src.base.utils.types import UUIDString


class AudioSourceRepositoryRedisImpl(AudioSourceRepositoryI):
    def __init__(self, redis_client: aioredis.client.Redis) -> None:
        self._redis_client = redis_client

        self._cache = RedisCache(
            redis_client=self._redis_client,
            key=project_settings.AUDIO_SOURCE_CACHE_REDIS_KEY,
            max_size=project_settings.AUDIO_SOURCE_CACHE_MAX_SIZE
        )

    def _get_track_audio_sources_key(self, track_uuid: UUIDString) -> str:
        return f"{project_settings.AUDIO_SOURCES_FOR_TRACK_REDIS_KEY}:{track_uuid}"

    async def _get_track_audio_sources(self, track_uuid: UUIDString) -> RedisHSet:
        key = self._get_track_audio_sources_key(track_uuid)

        return RedisHSet(
            redis_client=self._redis_client,
            key=key,
            max_size=project_settings.AUDIO_SOURCE_CACHE_MAX_SIZE
        )

    async def _get_audio_source_uuids_for_track(self, track_uuid: UUIDString) -> list[UUIDString]:
        hset = await self._get_track_audio_sources(track_uuid)
        keys = await hset.get_keys()

        expired = []
        sources = []
        for timestamp in keys:
            if datetime.fromtimestamp(float(timestamp)) < datetime.now():
                expired.append(timestamp)
            else:
                if (cached := await hset.read_data(timestamp)) is not None:  # TODO: Do i really need to check it?
                    sources.append(cached)

        if expired:
            await hset.delete(*expired)

        return sources

    async def _save_track_audio_source(self, source: AudioSource, hset: RedisHSet) -> None:
        await self.cache_audio_source(source)
        await hset.write_data(str(source.created_at.timestamp()), source.uuid)

    async def cache_audio_source_for_track(self, track_uuid: UUIDString, audio_source: AudioSource) -> None:
        hset = await self._get_track_audio_sources(track_uuid)
        await self._save_track_audio_source(audio_source, hset)

    async def cache_audio_sources_for_track(self, track_uuid: UUIDString, audio_sources: Iterable[AudioSource]) -> None:
        hset = await self._get_track_audio_sources(track_uuid)
        await gather_all((self._save_track_audio_source(source, hset) for source in audio_sources))

    async def cache_audio_source(self, audio_source: AudioSource) -> None:
        await self._cache.write_schema(audio_source.uuid, audio_source)

    async def cache_audio_sources(self, audio_sources: Iterable[AudioSource]) -> None:
        await gather_all(self._cache.write_schema(audio_source.uuid, audio_source) for audio_source in audio_sources)

    async def get_cached_audio_sources_for_track(self, track_uuid: UUIDString) -> tuple[AudioSource, ...]:
        uuids = await self._get_audio_source_uuids_for_track(track_uuid)

        sources = []
        for uuid in uuids:
            if (cached := await self.get_cached_audio_source(uuid)) is not None:  # TODO: Do i really need to check it?
                sources.append(cached)

        return tuple(sources)

    async def get_cached_audio_source(self, uuid: UUIDString) -> Optional[AudioSource]:
        return await self._cache.read_schema(uuid, schema_cls=AudioSource)

from abc import abstractmethod, ABC
from typing import Optional

from redis import asyncio as aioredis

from src.app.main.common.redis.collections.abc.redis_map import AbstractRedisMap


class SizedRedisMap(AbstractRedisMap, ABC):
    def __init__(self, redis_client: aioredis.client.Redis, key: str, max_size: Optional[int] = None) -> None:
        super().__init__(redis_client, key)

        self._max_size: Optional[int] = max_size

    @abstractmethod
    async def _write_data(
            self,
            key: str,
            data: str,
            ttl: Optional[int] = None,
            raise_on_overflow: bool = False
    ) -> None:
        ...

    @abstractmethod
    async def _resolve_overflow(self) -> bool:
        ...

    async def is_full(self) -> bool:
        return self._max_size is not None and await self.get_size() > self._max_size

    async def write_data(
            self,
            key: str,
            data: str,
            ttl: Optional[int] = None,
            raise_on_overflow: bool = False
    ) -> None:
        if await self.is_full():
            if raise_on_overflow:
                raise OverflowError(f"Cache for key {self._base_key} overflow")

            if not await self._resolve_overflow():
                raise OverflowError("Failed to resolve overflow")

        await self._write_data(key, data, ttl=ttl, raise_on_overflow=raise_on_overflow)

import asyncio
import logging
from typing import Optional

from .base import SizedRedisMap

_logger = logging.getLogger(__name__)


class RedisCache(SizedRedisMap):
    def _get_full_key(self, key: str) -> str:
        return f"{self._base_key}:{key}"

    async def _resolve_overflow(self) -> bool:
        keys = await self.get_keys()
        await self.delete_many(*keys[:len(keys) // 2])

        return True

    async def _write_data(
            self,
            key: str,
            data: str,
            ttl: Optional[int] = None,
            raise_on_overflow: bool = False
    ) -> None:
        await self._redis_client.set(self._get_full_key(key), data, ttl)  # type: ignore

    async def read_data(self, key: str) -> Optional[str]:
        return await self._redis_client.get(self._get_full_key(key))  # type: ignore

    async def get_keys(self) -> tuple[str, ...]:
        return tuple([key async for key in self._redis_client.scan_iter(match=self._base_key)])  # type: ignore

    async def get_size(self) -> int:
        return len(await self.get_keys())

    async def delete(self, key: str) -> None:
        await self._redis_client.delete(self._get_full_key(key))  # type: ignore

    async def delete_many(self, *keys, wait: bool = True) -> None:
        task = asyncio.create_task(self._redis_client.delete(*map(self._get_full_key, keys)))  # type: ignore

        if wait:
            await task

    async def clear(self) -> None:
        await self._redis_client.delete(self._base_key)  # type: ignore

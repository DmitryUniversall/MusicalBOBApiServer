from typing import Optional

from .base import SizedRedisMap


class RedisHSet(SizedRedisMap):
    async def _resolve_overflow(self) -> bool:
        keys = await self.get_keys()
        await self._redis_client.hdel(self._base_key, *keys[:len(keys) // 2])  # type: ignore
        return True

    async def get_keys(self) -> tuple[str, ...]:
        return await self._redis_client.hkeys(self._base_key)  # type: ignore

    async def get_size(self) -> int:
        return await self._redis_client.hlen(self._base_key)  # type: ignore

    async def read_data(self, key: str) -> Optional[str]:
        return await self._redis_client.hget(self._base_key, key)  # type: ignore

    async def _write_data(
            self,
            key: str,
            data: str,
            ttl: Optional[int] = None,
            raise_on_overflow: bool = False
    ) -> None:
        await self._redis_client.hset(self._base_key, key, data)  # type: ignore

        if ttl is not None:
            await self._redis_client.expire(self._base_key, ttl)

    async def clear(self) -> None:
        await self._redis_client.delete(self._base_key)  # type: ignore

    async def delete(self, key: str) -> None:
        await self._redis_client.hdel(self._base_key, key)  # type: ignore

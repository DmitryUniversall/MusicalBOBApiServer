from redis import asyncio as aioredis

from src.base.state import project_settings


class RedisClientFactory:
    def __init__(self) -> None:
        self._clients: dict[int, aioredis.Redis] = {}

    async def get_client(self, db: int = 0) -> aioredis.Redis:
        if db not in self._clients:
            self._clients[db] = await aioredis.from_url(
                url=f"{project_settings.REDIS_BASE_URL}{db}/",
                encoding=project_settings.REDIS_ENCODING,
                decode_responses=True
            )

        return self._clients[db]

    async def close_all(self) -> None:
        for client in self._clients.values():
            await client.close()

        self._clients.clear()

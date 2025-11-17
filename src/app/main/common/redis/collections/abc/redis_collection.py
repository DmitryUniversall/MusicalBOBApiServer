from abc import ABC

from redis import asyncio as aioredis


class AbstractRedisCollection(ABC):
    def __init__(self, redis_client: aioredis.client.Redis) -> None:
        self._redis_client: aioredis.client.Redis = redis_client

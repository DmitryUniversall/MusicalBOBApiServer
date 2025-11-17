import asyncio
import json
from abc import abstractmethod
from typing import Optional

from redis import asyncio as aioredis

from src.app.core import BaseSchema
from src.app.main.common.redis.collections.abc.redis_collection import AbstractRedisCollection
from src.base.utils.types import JsonDict


class AbstractRedisMap(AbstractRedisCollection):
    def __init__(self, redis_client: aioredis.client.Redis, key: str) -> None:
        super().__init__(redis_client)

        self._base_key: str = key

    @abstractmethod
    async def get_keys(self) -> tuple[str, ...]:
        ...

    @abstractmethod
    async def get_size(self) -> int:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...

    @abstractmethod
    async def read_data(self, key: str) -> Optional[str]:
        ...

    @abstractmethod
    async def write_data(
            self,
            key: str,
            data: str,
            ttl: Optional[int] = None
    ) -> None:
        ...

    async def read_json(self, key: str) -> Optional[JsonDict]:
        if (data := await self.read_data(key)) is None:
            return None

        return json.loads(data)

    async def read_schema[T: BaseSchema](self, key: str, *, schema_cls: type[T]) -> Optional[T]:
        if (json_data := await self.read_json(key)) is None:
            return None

        return schema_cls.model_validate(json_data)

    async def read_data_strict(self, key: str) -> str:
        if (result := await self.read_data(key)) is None:
            raise KeyError(f"Failed to find cached value for key '{key}'")

        return result

    async def read_json_strict(self, key: str) -> JsonDict:
        if (result := await self.read_json(key)) is None:
            raise KeyError(f"Failed to find cached value for key '{key}'")

        return result

    async def read_schema_strict[T: BaseSchema](self, key: str, *, schema_cls: type[T]) -> T:
        if (result := await self.read_schema(key, schema_cls=schema_cls)) is None:
            raise KeyError(f"Failed to find cached value for key '{key}'")

        return result

    async def write_json(
            self,
            key: str,
            data: JsonDict,
            ttl: Optional[int] = None
    ) -> None:
        await self.write_data(key, json.dumps(data), ttl=ttl)

    async def write_schema(  # TODO: Use generic
            self,
            key: str,
            schema: BaseSchema,
            ttl: Optional[int] = None
    ) -> None:
        await self.write_data(key, schema.model_dump_json(), ttl=ttl)

    async def delete_many(self, *keys, wait: bool = False) -> None:
        tasks = (asyncio.create_task(self.delete(key)) for key in keys)
        if wait:
            await asyncio.wait(tasks)

from abc import ABC, abstractmethod


class AbstractComponentService(ABC):
    @abstractmethod
    async def setup(self) -> None:
        pass

from abc import ABC, abstractmethod

from src.base.utils.interface import InterfaceMeta


class TranslationRepositoryI(ABC, metaclass=InterfaceMeta):
    @abstractmethod
    async def translate(self, text: str, language_code: str, source_code: str) -> str:
        ...

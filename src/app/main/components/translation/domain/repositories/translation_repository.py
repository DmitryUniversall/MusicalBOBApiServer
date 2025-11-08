from abc import ABC, abstractmethod


class TranslationRepositoryI(ABC):
    @abstractmethod
    async def translate(self, text: str, language_code: str, source_code: str) -> str:
        ...

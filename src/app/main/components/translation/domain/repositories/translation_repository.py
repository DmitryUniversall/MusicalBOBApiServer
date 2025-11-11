from abc import ABC, abstractmethod
from typing import Iterable

from googletrans.models import Translated


class TranslationRepositoryI(ABC):
    @abstractmethod
    async def translate(self, text: str, language_code: str, source_code: str) -> Translated:
        ...

    @abstractmethod
    async def translate_to_text(self, text: str, language_code: str, source_code: str) -> str:
        ...

    @abstractmethod
    async def translate_many(self, text: str, language_codes: Iterable[str], source_code: str) -> tuple[Translated, ...]:
        ...

    @abstractmethod
    async def translate_many_to_text(self, text: str, language_codes: Iterable[str], source_code: str) -> dict[str, str]:
        ...

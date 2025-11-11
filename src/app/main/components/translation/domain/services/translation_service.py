from abc import ABC, abstractmethod
from typing import Iterable


class TranslationServiceI(ABC):
    @abstractmethod
    async def translate_to_text(self, text: str, language_code: str, source_code: str = 'auto') -> str:
        ...

    @abstractmethod
    async def translate_many_to_text(self, text: str, language_codes: Iterable[str], source_code: str = 'auto') -> dict[str, str]:
        ...

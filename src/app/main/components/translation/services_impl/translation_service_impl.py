from typing import Iterable

from src.app.main.components.translation.domain import TranslationServiceI, TranslationRepositoryI


class TranslationServiceImpl(TranslationServiceI):
    def __init__(self, translation_repository: TranslationRepositoryI) -> None:
        self._translation_repository: TranslationRepositoryI = translation_repository

    async def translate_to_text(self, text: str, language_code: str, source_code: str = 'auto') -> str:
        return await self._translation_repository.translate_to_text(text, language_code, source_code=source_code)

    async def translate_many_to_text(self, text: str, language_codes: Iterable[str], source_code: str = 'auto') -> dict[str, str]:
        return await self._translation_repository.translate_many_to_text(text, language_codes, source_code=source_code)

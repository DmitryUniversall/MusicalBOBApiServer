import asyncio

from googletrans import Translator

from src.app.main.components.translation.domain import TranslationRepositoryI


class TranslationRepositoryImpl(TranslationRepositoryI):
    def __init__(self) -> None:
        self._translator = Translator()

    async def _translate_async(self, text: str, language_code: str, source_code: str) -> str:
        return await asyncio.to_thread(self._translator.translate, text, dest=language_code, src=source_code)

    async def translate(self, text: str, language_code: str, source_code: str) -> str:
        return await self._translate_async(text, language_code, source_code)

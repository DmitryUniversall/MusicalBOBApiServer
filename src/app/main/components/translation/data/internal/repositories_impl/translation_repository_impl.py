from typing import Iterable

from googletrans import Translator
from googletrans.models import Translated

from src.app.main.components.translation.domain import TranslationRepositoryI
from src.app.main.components.translation.domain.exceptions import InvalidLanguageHTTPException
from src.base.utils.async_tools import gather_all


class TranslationRepositoryImpl(TranslationRepositoryI):
    def __init__(self, translator: Translator) -> None:
        self._translator: Translator = translator

    async def translate(self, text: str, language_code: str, source_code: str) -> Translated:
        try:
            return await self._translator.translate(text, dest=language_code, src=source_code)  # type: ignore
        except ValueError as error:
            raise InvalidLanguageHTTPException(message=str(error)) from error

    async def translate_to_text(self, text: str, language_code: str, source_code: str) -> str:
        translated: Translated = await self.translate(text, language_code, source_code)
        return translated.text

    async def translate_many(self, text: str, language_codes: Iterable[str], source_code: str) -> tuple[Translated, ...]:
        return await gather_all(self.translate(text, language_code, source_code) for language_code in language_codes)

    async def translate_many_to_text(self, text: str, language_codes: Iterable[str], source_code: str) -> dict[str, str]:
        translations: tuple[Translated, ...] = await self.translate_many(text, language_codes, source_code)
        return {translation.dest: translation.text for translation in translations}

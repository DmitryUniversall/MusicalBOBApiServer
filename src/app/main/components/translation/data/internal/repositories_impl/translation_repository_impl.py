from googletrans import Translator

from src.app.main.components.translation.domain import TranslationRepositoryI
from src.app.main.components.translation.domain.exceptions import InvalidLanguageHTTPException


class TranslationRepositoryImpl(TranslationRepositoryI):
    def __init__(self, translator: Translator) -> None:
        self._translator: Translator = translator

    async def _translate_async(self, text: str, language_code: str, source_code: str) -> str:  # TODO: Add method to translate to N languages asynchronously
        try:
            translation = await self._translator.translate(text, dest=language_code, src=source_code)
        except ValueError as error:
            raise InvalidLanguageHTTPException(message=str(error)) from error

        return translation.text

    async def translate(self, text: str, language_code: str, source_code: str) -> str:
        return await self._translate_async(text, language_code, source_code)

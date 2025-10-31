from src.app.main.components.translation.domain import TranslationServiceI, TranslationRepositoryI


class TranslationServiceImpl(TranslationServiceI):
    def __init__(self) -> None:
        self._translation_repository: TranslationRepositoryI = TranslationRepositoryI.get_implementation()  # type: ignore

    async def translate(self, text: str, language_code: str, source_code: str = 'auto') -> str:
        return await self._translation_repository.translate(text, language_code, source_code=source_code)

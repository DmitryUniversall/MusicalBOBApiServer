from src.app.core import BaseSchema
from src.app.main.common.utils.localizations import LanguageCode


class Lyrics(BaseSchema):
    lyrics: str
    translations: dict[LanguageCode, str] = {}

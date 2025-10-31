from src.app.core import BaseSchema


class LyricsSearchResult(BaseSchema):
    lyrics: str
    translations: dict[str, str]

from src.app.core import BaseSchema
from src.app.main.components.common_search import Lyrics


class LyricsSearchResult(BaseSchema):
    lyrics: Lyrics

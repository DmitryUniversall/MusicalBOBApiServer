from typing import Optional

from src.app.core import BaseSchema


class LyricsSearchResult(BaseSchema):
    lyrics: Optional[str] = None
    translations: Optional[dict[str, str]] = None

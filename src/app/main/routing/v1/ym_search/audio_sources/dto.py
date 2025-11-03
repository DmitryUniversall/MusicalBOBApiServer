from src.app.core import BaseSchema
from src.app.main.components.common_search import AudioSource


class AudioSourcesSearchResult(BaseSchema):
    audio_sources: tuple[AudioSource, ...]

from src.app.core import BaseSchema
from src.app.main.components.audio_sources import AudioSource


class AudioSourceSearchResult(BaseSchema):
    audio_sources: tuple[AudioSource, ...]

from datetime import datetime, timedelta
from uuid import uuid4

from pydantic import Field

from src.app.core import BaseSchema
from src.base.state import project_settings
from src.base.utils.types import UUIDString


class AudioSource(BaseSchema):
    source: str
    uuid: UUIDString = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(seconds=project_settings.AUDIO_SOURCE_DEFAULT_TTL))

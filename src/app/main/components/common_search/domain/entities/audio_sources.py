from datetime import datetime

from pydantic import Field

from src.app.core import BaseSchema


class AudioSource(BaseSchema):
    created_at: datetime = Field(default_factory=datetime.now)
    source: str

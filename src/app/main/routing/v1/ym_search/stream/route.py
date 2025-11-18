from typing import AsyncGenerator

import aiohttp
from dependency_injector.wiring import Provide
from fastapi import Depends
from starlette.requests import Request
from starlette.responses import StreamingResponse

from src.app.core import route_inject
from src.app.main.common import BadRequestHTTPException
from src.app.main.common.utils.auth import auth_protected
from src.app.main.components.audio_sources import AudioSourceServiceI
from src.app.main.di import GlobalContainer
from .exceptions import InvalidAudioSourceToStreamHTTPException
from ..component_router_v1 import ym_search_router_v1


@ym_search_router_v1.get("/stream", dependencies=[Depends(auth_protected)], response_model=None)
@route_inject(
    _audio_source_service=Depends(Provide[GlobalContainer.shortcut_audio_source_service])
)
async def stream_audio_source(
        request: Request,
        audio_source_uuid: str,
        _audio_source_service: AudioSourceServiceI
) -> StreamingResponse:
    headers = {}
    media_type = "audio/mpeg"

    if (cached_audio_source := await _audio_source_service.get_cached_audio_source(audio_source_uuid)) is None:
        raise InvalidAudioSourceToStreamHTTPException()

    if range_header := request.headers.get("range"):
        headers["Range"] = range_header

    async def _streamer() -> AsyncGenerator[bytes, None]:
        nonlocal media_type

        session_timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            async with session.get(cached_audio_source.source, headers=headers) as response:
                media_type = response.headers.get("Content-Type", media_type)

                if response.status != 200 and response.status != 206:
                    raise BadRequestHTTPException(message=f"Failed to get audio from specified url: {response.status}")

                async for chunk in response.content.iter_chunked(8192):
                    yield chunk

    return StreamingResponse(_streamer(), media_type=media_type)

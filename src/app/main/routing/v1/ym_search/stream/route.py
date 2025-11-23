import asyncio
import logging
from enum import Enum
from typing import AsyncGenerator, Optional, cast

import aiohttp
from dependency_injector.wiring import Provide
from fastapi import Depends
from starlette.requests import Request
from starlette.responses import StreamingResponse

from src.app.core import route_inject
from src.app.main.common.utils.auth import HTTPJWTBearerAuthDependency
from src.app.main.components.audio_sources import AudioSourceServiceI, AudioSource
from src.app.main.components.auth import AuthServiceI
from src.app.main.di import GlobalContainer
from src.base.utils.async_tools import TempTask
from .exceptions import InvalidAudioSourceToStreamHTTPException, FailedToReadOriginalAudioSourceHTTPException
from ..component_router_v1 import ym_search_router_v1

_logger = logging.getLogger(__name__)

type _AudioDownloaderQueue = asyncio.Queue[tuple[_AudioReaderEvent, Optional[bytes | Exception]]]


class _AudioReaderEvent(Enum):
    START = 0
    DATA = 1
    ERROR = 2
    END = 3


async def _chunk_reader(response: aiohttp.ClientResponse):
    async for chunk in response.content.iter_any():
        yield chunk


async def _buffered_audio_downloader(audio_source: AudioSource, queue: _AudioDownloaderQueue, headers: dict) -> None:
    session_timeout = aiohttp.ClientTimeout(total=None)

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        try:
            response = await session.get(audio_source.source, headers=headers)

            if response.status != 200 and response.status != 206:
                await queue.put((_AudioReaderEvent.ERROR, FailedToReadOriginalAudioSourceHTTPException(audio_source.uuid, response.status)))
                return

            await queue.put((_AudioReaderEvent.START, None))

            async for chunk in _chunk_reader(response):
                await queue.put((_AudioReaderEvent.DATA, chunk))
        except Exception as error:
            await queue.put((_AudioReaderEvent.ERROR, error))
        finally:
            await queue.put((_AudioReaderEvent.END, None))


async def _buffered_audio_streamer(audio_source: AudioSource, request_headers: dict) -> AsyncGenerator[bytes, None]:
    queue: _AudioDownloaderQueue = asyncio.Queue(maxsize=10)

    async with TempTask(_buffered_audio_downloader(audio_source, queue, request_headers)):
        while (event := await queue.get()) is not None:
            match event[0]:
                case _AudioReaderEvent.START:
                    _logger.debug(f"Start streaming audio source '{audio_source.uuid}'. Using source: {audio_source.source}")
                case _AudioReaderEvent.DATA:
                    data = cast(bytes, event[1])
                    yield data
                case _AudioReaderEvent.ERROR:
                    error = cast(Exception, event[1])
                    _logger.warning(f"Failed to stream audio source '{audio_source.uuid}'. Got an error: {error}")
                    return
                case _AudioReaderEvent.END:
                    _logger.debug(f"Finished streaming audio source '{audio_source.uuid}'")
                    return


@ym_search_router_v1.get("/stream", response_model=None)
@route_inject(
    _audio_source_service=Depends(Provide[GlobalContainer.shortcut_audio_source_service]),
    _auth_service=Depends(Provide[GlobalContainer.shortcut_auth_service])
)
async def stream_audio_source(
        request: Request,
        audio_source_uuid: str,
        token: str,
        _audio_source_service: AudioSourceServiceI,
        _auth_service: AuthServiceI
) -> StreamingResponse:
    # Pass auth token via parameter for audio source url to be fully constructed to use it with ffmpeg or tools like that
    jwt_auth = HTTPJWTBearerAuthDependency(_auth_service)
    await jwt_auth(request, access_token=token)

    if (cached_audio_source := await _audio_source_service.get_cached_audio_source(audio_source_uuid)) is None:
        raise InvalidAudioSourceToStreamHTTPException()

    base_source_request_headers = {}
    if range_header := request.headers.get("range"):
        base_source_request_headers["Range"] = range_header

    return StreamingResponse(
        _buffered_audio_streamer(cached_audio_source, base_source_request_headers),
        media_type="audio/mpeg",
        headers={
            "Transfer-Encoding": "chunked",
        }
    )

from typing import AsyncGenerator

import aiohttp
from starlette.requests import Request
from starlette.responses import StreamingResponse

from src.app.main.common import BadRequestHTTPException, InternalServerErrorHTTPException
from ..component_router_v1 import ym_search_router_v1


@ym_search_router_v1.get("/stream")
async def stream_audio_source(request: Request, url: str) -> StreamingResponse:
    if not url.startswith("https://api.music.yandex.net/"):
        raise BadRequestHTTPException(message="Invalid URL specified. This endpoint only allows to stream tracks from the yandex music api server")

    headers = {}
    media_type = "audio/mpeg"

    if range_header := request.headers.get("range"):
        headers["Range"] = range_header

    async def _streamer() -> AsyncGenerator[bytes, None]:
        nonlocal media_type

        session_timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            async with session.get(url, headers=headers) as response:
                media_type = response.headers.get("Content-Type", media_type)

                if response.status != 200 and response.status != 206:
                    raise BadRequestHTTPException(message=f"Failed to get audio from specified url: {response.status}")

                async for chunk in response.content.iter_chunked(8192):
                    yield chunk

    return StreamingResponse(_streamer(), media_type=media_type)

import logging

from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from src.app.core.exceptions import AbstractErrorHandler
from src.app.main.common.http import ApplicationJsonResponse

_logger = logging.getLogger(__name__)


@AbstractErrorHandler.as_error_handler(exception_cls=StarletteHTTPException)
async def starlette_exception_handler(request: Request, error: StarletteHTTPException, **__) -> ApplicationJsonResponse:
    # We can use http_exception_handler and be sure that it will return ApplicationJsonResponse because
    return await http_exception_handler(request, error)  # type: ignore

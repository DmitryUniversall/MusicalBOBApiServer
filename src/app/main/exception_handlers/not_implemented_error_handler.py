import logging
from http import HTTPStatus

from starlette.requests import Request

from src.app.core.exceptions import AbstractErrorHandler
from src.app.main.common.dto import ApplicationResponseDTO
from src.app.main.common.http import ApplicationJsonResponse
from src.base.state import project_settings
from src.base.utils.types import JsonDict

_logger = logging.getLogger(__name__)


@AbstractErrorHandler.as_error_handler(exception_cls=NotImplementedError)
async def not_implemented_exception_handler(_: Request, error: NotImplementedError, **__) -> ApplicationJsonResponse:
    _logger.debug(f"Sending HTTP 501 on error: {error.__class__.__name__}: {error}")

    return ApplicationJsonResponse(
        content=ApplicationResponseDTO[JsonDict](
            ok=False,
            data=None,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.NOT_IMPLEMENTED
        ),
        status_code=HTTPStatus.NOT_IMPLEMENTED
    )

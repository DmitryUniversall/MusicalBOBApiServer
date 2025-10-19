import logging
from http import HTTPStatus

from starlette.requests import Request

from src.app.core.exceptions import AbstractErrorHandler
from src.app.main.common.http import ApplicationJsonResponse
from src.app.main.common.models import ApplicationResponsePayload
from src.base.exceptions import AlreadyExistsError
from src.base.state import project_settings
from src.base.utils.types import JsonDict

_logger = logging.getLogger(__name__)


@AbstractErrorHandler.as_error_handler(exception_cls=AlreadyExistsError)
async def already_exist_exception_handler(_: Request, error: AlreadyExistsError, **__) -> ApplicationJsonResponse:
    _logger.debug(f"Sending HTTP 409 on error: {error.__class__.__name__}: {error}")

    return ApplicationJsonResponse(
        content=ApplicationResponsePayload[JsonDict](
            ok=False,
            data=None,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.ALREADY_EXISTS
        ),
        status_code=HTTPStatus.CONFLICT
    )

import logging
from http import HTTPStatus

from starlette.requests import Request

from src.app.core import DBDoesNotExistError
from src.app.core.exceptions import AbstractErrorHandler
from src.app.main.common.http import ApplicationJsonResponse
from src.app.main.common.models import ApplicationResponsePayload
from src.base.state import project_settings
from src.base.utils.types import JsonDict

_logger = logging.getLogger(__name__)


@AbstractErrorHandler.as_error_handler(exception_cls=DBDoesNotExistError)
async def does_not_exist_exception_handler(_: Request, error: DBDoesNotExistError, **__) -> ApplicationJsonResponse:
    _logger.debug(f"Sending HTTP 404 on error: {error.__class__.__name__}: {error}")

    return ApplicationJsonResponse(
        content=ApplicationResponsePayload[JsonDict](
            ok=False,
            application_status_code=project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.NOT_FOUND,
            message="Object or sub-object does not exist",
            data=None
        ),
        status_code=HTTPStatus.NOT_FOUND
    )

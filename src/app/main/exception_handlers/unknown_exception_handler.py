from http import HTTPStatus

from src.app.core.exceptions import AbstractErrorHandler
from src.app.main.common.http import ApplicationJsonResponse
from src.app.main.common.models import ApplicationResponsePayload
from src.base.state import project_settings


@AbstractErrorHandler.as_error_handler(exception_cls=Exception)
async def unknown_exception_handler(*_, **__) -> ApplicationJsonResponse:
    return ApplicationJsonResponse(
        content=ApplicationResponsePayload(
            ok=False,
            data=None,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.INTERNAL_SERVER_ERROR,
        ),
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    )

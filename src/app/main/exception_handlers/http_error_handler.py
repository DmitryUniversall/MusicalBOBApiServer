from http import HTTPStatus

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from src.app.core.exceptions import AbstractErrorHandler
from src.app.main.common.http import ApplicationJsonResponse
from src.app.main.common.models import ApplicationResponsePayload
from src.base.state import project_settings
from src.base.utils.types import JsonDict


async def _handle_unknown_route_error() -> ApplicationJsonResponse:
    return ApplicationJsonResponse(
        content=ApplicationResponsePayload[JsonDict](
            ok=False,
            data=None,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.ROUTE_DOES_NOT_EXISTS,
        ),
        status_code=HTTPStatus.NOT_FOUND
    )


@AbstractErrorHandler.as_error_handler(exception_cls=StarletteHTTPException)
async def http_exception_handler(_: Request, error: StarletteHTTPException, **__) -> ApplicationJsonResponse:
    if error.status_code == 404:
        return await _handle_unknown_route_error()

    return ApplicationJsonResponse(
        content=ApplicationResponsePayload[JsonDict](
            ok=200 <= error.status_code < 300,
            application_status_code=project_settings.APPLICATION_STATUS_CODES.NOT_SPECIFIED,
            message=str(error),
            data={
                "detail": error.detail
            }
        ),
        status_code=error.status_code,
        headers=error.headers
    )

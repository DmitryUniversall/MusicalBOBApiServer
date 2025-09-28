from starlette.exceptions import HTTPException
from starlette.requests import Request

from src.app.core.exceptions import AbstractErrorHandler
from src.app.main.common.http import ApplicationJsonResponse
from src.app.main.common.models import ApplicationResponsePayload
from src.base.state import project_settings
from src.base.utils.types import JsonDict


@AbstractErrorHandler.as_error_handler(exception_cls=HTTPException)
async def http_exception_handler(_: Request, error: HTTPException, **__) -> ApplicationJsonResponse:
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

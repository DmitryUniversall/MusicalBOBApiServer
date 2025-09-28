from http import HTTPStatus

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from src.app.core.exceptions import AbstractErrorHandler
from src.app.main.common.http import ApplicationJsonResponse
from src.app.main.common.models import ApplicationResponsePayload
from src.base.state import project_settings
from src.base.utils.types import JsonDict


@AbstractErrorHandler.as_error_handler(exception_cls=RequestValidationError)
async def http_validation_exception_handler(_: Request, exc: RequestValidationError, **__) -> ApplicationJsonResponse:
    return ApplicationJsonResponse(
        content=ApplicationResponsePayload[JsonDict](
            ok=False,
            data={"detail": jsonable_encoder(exc.errors())},
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.UNPROCESSABLE_ENTITY
        ),
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY
    )

# @AbstractErrorHandler.as_error_handler(exception_cls=WebSocketRequestValidationError)  TODO
# async def request_validation_exception_handler(websocket: WebSocket, exc: WebSocketRequestValidationError, **__) -> CustomJsonResponse:
#     await websocket.close(
#         code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
#     )
#
#     return CustomJsonResponse(
#         **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.UNPROCESSABLE_ENTITY,
#         status_code=422,
#         content={"errors": jsonable_encoder(exc.errors())}
#     )
#
#
# async def websocket_request_validation_exception_handler(
#         websocket: WebSocket, exc: WebSocketRequestValidationError
# ) -> None:
#     await websocket.close(
#         code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
#     )

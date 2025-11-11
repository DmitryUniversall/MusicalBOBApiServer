from starlette.responses import StreamingResponse

from src.app.core.http.routing import AbstractStaticResponseTypeApiRoute, ResponseTypeValidatorApiRoute
from src.app.main.common.http.responses import ApplicationJsonResponse


class ApplicationResponseApiRoute(AbstractStaticResponseTypeApiRoute[ApplicationJsonResponse]):
    """
    A route handler class for FastAPI that enforces the response type to be `ApplicationJsonResponse`
    """

    __response_type__: type[ApplicationJsonResponse] = ApplicationJsonResponse


class StreamableApplicationResponseApiRoute(ResponseTypeValidatorApiRoute):
    """
    A route handler class for FastAPI that enforces the response type to be `ApplicationJsonResponse` or `StreamingResponse`
    """

    __allowed_response_types__ = (ApplicationJsonResponse, StreamingResponse)

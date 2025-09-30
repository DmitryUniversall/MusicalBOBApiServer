from src.app.core.http.routing import AbstractStaticResponseTypeApiRoute
from src.app.main.common.http.responses import ApplicationJsonResponse


class ApplicationResponseApiRoute(AbstractStaticResponseTypeApiRoute[ApplicationJsonResponse]):
    """
    A route handler class for FastAPI that enforces the response type to be `ApplicationJsonResponse`.
    """

    __response_type__: type[ApplicationJsonResponse] = ApplicationJsonResponse

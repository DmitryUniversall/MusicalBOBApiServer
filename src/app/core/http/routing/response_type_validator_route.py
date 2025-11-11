from abc import ABC, abstractmethod
from typing import Coroutine, Any, Callable

from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute


class ResponseTypeValidatorApiRoute(APIRoute, ABC):
    """
    An abstract base class for FastAPI routes that enforce a specific response type.
    """

    @property
    @abstractmethod
    def __allowed_response_types__(self) -> tuple[type[Response], ...]:
        """
        Abstract property that defines allowed response types for the route

        :return: `tuple[type[Response], ...]`
            The allowed types of the response from the route handler
        """

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        """
        Overrides the FastAPI `get_route_handler` method to ensure the response is of the expected type

        :return: `Callable[[Request], Coroutine[Any, Any, Response]]`
            A callable that handles the route and ensures the response is of the expected type
        """

        original_handler = super().get_route_handler()

        async def custom_handler(request: Request) -> Response:
            response = await original_handler(request)

            if not isinstance(response, self.__allowed_response_types__):
                raise TypeError(
                    f"[{self.__class__.__name__}]: Unexpected response type: must be one instance of {self.__allowed_response_types__}"
                )

            return response

        return custom_handler

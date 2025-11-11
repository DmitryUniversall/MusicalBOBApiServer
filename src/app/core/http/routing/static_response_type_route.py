from abc import ABC, abstractmethod
from typing import Callable, Coroutine, Any

from fastapi.responses import Response
from starlette.requests import Request

from .response_type_validator_route import ResponseTypeValidatorApiRoute


class AbstractStaticResponseTypeApiRoute[_responseT: Response](ResponseTypeValidatorApiRoute, ABC):
    """
    An abstract base class for FastAPI routes that enforce a specific response type.
    """

    @property
    @abstractmethod
    def __response_type__(self) -> type[_responseT]:
        """
        Abstract property that defines the expected response type for the route.

        :return: `type[_responseT]`
            The type of the response expected from the route handler
        """

    @property
    def __allowed_response_types__(self) -> tuple[type[_responseT]]:
        return (self.__response_type__,)

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        """
        Overrides `get_route_handler` method to ensure the response is of the expected type (only 1 allowed)

        :return: `Callable[[Request], Coroutine[Any, Any, Response]]`
            A callable that handles the route and ensures the response is of the expected type (only 1 allowed)
        """

        if len(self.__allowed_response_types__) != 1:
            raise TypeError("AbstractStaticResponseTypeApiRoute must have exactly one allowed response type")

        return super().get_route_handler()

import inspect
from functools import wraps
from inspect import Parameter

from starlette.responses import JSONResponse

from .types import RouteCoro, RouteCoroDecorator  # type: ignore


def route_inject[T: JSONResponse](**requested):  # FIXME: returns RouteCoroDecorator[T] but annotation cause mypy error
    def decorator(coro: RouteCoro[T]) -> RouteCoro[T]:
        original_signature = inspect.signature(coro)
        original_parameters = tuple(original_signature.parameters.values())

        new_parameters = []
        update_parameters_count = 0
        for parameter in original_parameters:
            if parameter.name not in requested:
                new_parameters.append(parameter)
                continue

            update_parameters_count += 1
            new_parameters.append(Parameter(
                name=parameter.name,
                annotation=parameter.annotation,
                kind=parameter.kind,
                default=requested[parameter.name],
            ))

        if update_parameters_count != len(requested):
            raise TypeError("All parameters that should be injected must be present in original signature")

        new_signature = original_signature.replace(parameters=new_parameters)

        @wraps(coro)
        async def wrapper(*args, **kwargs) -> T:
            return await coro(*args, **kwargs)

        wrapper.__signature__ = new_signature  # type: ignore[attr-defined]
        return wrapper

    return decorator

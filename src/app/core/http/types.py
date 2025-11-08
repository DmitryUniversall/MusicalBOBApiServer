from typing import Callable, Awaitable

from starlette.responses import JSONResponse

type RouteCoro[T: JSONResponse] = Callable[..., Awaitable[T]]
type RouteCoroDecorator[T: JSONResponse] = Callable[[RouteCoro[T]], RouteCoro[T]]

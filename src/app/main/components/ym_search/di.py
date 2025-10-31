from .data import di  # type: ignore

from .domain import YMSearchServiceI
from .services_impl import YMSearchServiceImpl

YMSearchServiceI.bind_implementation(YMSearchServiceImpl)  # type: ignore

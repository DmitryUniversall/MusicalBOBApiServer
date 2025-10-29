from .data import di  # type: ignore

from .domain import UsersServiceI
from .services_impl import UsersServiceImpl

UsersServiceI.bind_implementation(UsersServiceImpl)  # type: ignore

from .service import UsersService
from .service_impl import UsersServiceImpl

UsersService.bind_implementation(UsersServiceImpl)

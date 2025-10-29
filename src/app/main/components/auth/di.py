from .data import di  # type: ignore

from .domain.services.auth_service import AuthServiceI
from .domain.services.auth_session_service import AuthSessionServiceI
from .services_impl.auth_service_impl import AuthServiceImpl
from .services_impl.auth_session_service_impl import AuthSessionServiceImpl

AuthSessionServiceI.bind_implementation(AuthSessionServiceImpl)  # type: ignore
AuthServiceI.bind_implementation(AuthServiceImpl)  # type: ignore

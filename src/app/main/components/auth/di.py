from .data import di  # type: ignore

from .domain.services.auth_service import AuthService
from .domain.services.auth_session_service import AuthSessionService
from .services_impl.auth_service_impl import AuthServiceImpl
from .services_impl.auth_session_service_impl import AuthSessionServiceImpl

AuthSessionService.bind_implementation(AuthSessionServiceImpl)
AuthService.bind_implementation(AuthServiceImpl)

from src.app.main.components.auth.domain import AuthSessionService, AuthSessionServiceImpl
from src.app.main.components.auth.domain.services.auth_service import AuthService
from src.app.main.components.auth.domain.services_impl.auth_service_impl import AuthServiceImpl

AuthSessionService.bind_implementation(AuthSessionServiceImpl)
AuthService.bind_implementation(AuthServiceImpl)

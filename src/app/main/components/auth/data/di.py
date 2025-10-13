from src.app.main.components.auth.data.internal.repositories import AuthSessionRepositoryRedisImpl
from src.app.main.components.auth.domain import AuthSessionRepository

AuthSessionRepository.bind_implementation(AuthSessionRepositoryRedisImpl)

from src.app.main.components.auth.data.internal.repositories import AuthSessionRepositoryRedisImpl
from src.app.main.components.auth.domain import AuthSessionRepositoryI

AuthSessionRepositoryI.bind_implementation(AuthSessionRepositoryRedisImpl)

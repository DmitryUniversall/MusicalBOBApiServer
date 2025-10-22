from src.app.main.components.users.data.internal.repositories_impl import UsersRepositoryImpl
from src.app.main.components.users.domain import UsersRepositoryI

UsersRepositoryI.bind_implementation(UsersRepositoryImpl)

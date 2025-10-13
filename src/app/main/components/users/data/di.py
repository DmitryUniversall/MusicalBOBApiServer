from src.app.main.components.users.data.internal.repositories import UsersRepositoryImpl
from src.app.main.components.users.domain import UsersRepository

UsersRepository.bind_implementation(UsersRepositoryImpl)

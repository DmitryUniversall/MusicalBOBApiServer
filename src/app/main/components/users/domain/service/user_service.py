from src.app.main.components.users.domain.repository.user_repositry import UsersRepository


class UsersService:
    def __init__(self, user_repository: UsersRepository) -> None:
        self._user_repository = user_repository

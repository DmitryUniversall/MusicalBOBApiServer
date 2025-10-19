from src.app.main.common.db.exceptions import UniqueConstraintFailed
from src.app.main.components.users.data.internal.adapters import UserModelAdapter
from src.app.main.components.users.data.internal.models import UserModel
from src.app.main.components.users.domain import UsersRepository, UserInternal
from src.base.exceptions import DoesNotExistError, AlreadyExistsError


class UsersRepositoryImpl(UsersRepository):
    def __init__(self) -> None:
        self._user_model_adapter = UserModelAdapter()

    async def create_user(self, username: str, password_hashed: str, **fields) -> UserInternal:
        try:
            user_model = UserModel(username=username, password=password_hashed, **fields)
            await self._user_model_adapter.create(user_model)
            return user_model.to_schema(UserInternal)
        except UserModel.DoesNotExist as error:
            raise DoesNotExistError(f"User does not exists") from error
        except UniqueConstraintFailed as error:
            raise AlreadyExistsError(f"User already exists") from error

    async def get_user_by_id(self, user_id: int) -> UserInternal:
        try:
            user_model = await self._user_model_adapter.get_by_pk_strict(user_id)
            return user_model.to_schema(UserInternal)
        except UserModel.DoesNotExist as error:
            raise DoesNotExistError(f"User does not exists") from error

    async def get_user_by_username(self, username: str, **fields) -> UserInternal:
        try:
            user_model = await self._user_model_adapter.get_one_by_strict(username=username, **fields)
            return user_model.to_schema(UserInternal)
        except UserModel.DoesNotExist as error:
            raise DoesNotExistError(f"User does not exists") from error

    async def get_user_by_auth_credentials(self, username: str, password_hashed: str, **fields) -> UserInternal:
        try:
            user_model = await self._user_model_adapter.get_one_by_strict(username=username, password=password_hashed, **fields)
            return user_model.to_schema(UserInternal)
        except UserModel.DoesNotExist as error:
            raise DoesNotExistError(f"User does not exists") from error

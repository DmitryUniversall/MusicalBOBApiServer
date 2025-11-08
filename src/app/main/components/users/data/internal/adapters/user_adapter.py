from src.app.core.db import ObservableModelAdapter
from src.app.main.common.db import AsyncDatabaseManagerST
from ..models.user import UserModel


class UserModelAdapter(ObservableModelAdapter[UserModel, int]):
    __model_cls__: type[UserModel] = UserModel
    __db_manager__: AsyncDatabaseManagerST = AsyncDatabaseManagerST()

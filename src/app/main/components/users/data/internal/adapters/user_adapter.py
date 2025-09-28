from src.app.core.db import ObservableModelAdapter
from src.app.main.common.db import AsyncDatabaseManagerST
from src.base.utils.singleton import ABCSingletonMeta
from ..models.user import UserModel


class UserModelAdapter(ObservableModelAdapter[UserModel, int], metaclass=ABCSingletonMeta):
    __model_cls__: type[UserModel] = UserModel
    __db_manager__: AsyncDatabaseManagerST = AsyncDatabaseManagerST()

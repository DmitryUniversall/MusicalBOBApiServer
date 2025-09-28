from src.base.exceptions import BaseApplicationError, NotFoundError


class DBError(BaseApplicationError):
    pass


class DBDoesNotExistError(DBError, NotFoundError):
    pass

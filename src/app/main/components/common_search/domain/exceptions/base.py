from abc import ABC
from http import HTTPStatus

from src.app.main.common.http import GenericApplicationHTTPException


class SearchHTTPException(GenericApplicationHTTPException, ABC):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("status_code", HTTPStatus.BAD_REQUEST)
        super().__init__(**kwargs)

from abc import ABC

from src.app.main.common import GenericApplicationHTTPException


class TranslationHTTPException(GenericApplicationHTTPException, ABC):
    pass

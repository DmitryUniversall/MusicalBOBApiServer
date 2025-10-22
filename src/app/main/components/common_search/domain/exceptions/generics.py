from src.app.main.common import ApplicationResponsePayload
from src.base.state import project_settings
from .base import SearchHTTPException


class SearchFailedNotFoundHttpException(SearchHTTPException):
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.SEARCH.SEARCH_FAILED_NOT_FOUND,
            **payload_kwargs
        })


class BadUrlFormatHttpException(SearchHTTPException):
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.SEARCH.BAD_URL_FORMAT,
            **payload_kwargs
        })

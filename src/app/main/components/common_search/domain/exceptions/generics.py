from src.app.main.common import ApplicationResponseDTO
from src.base.state import project_settings
from .base import SearchHTTPException


class SearchFailedNotFoundHttpException(SearchHTTPException):
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.SEARCH.SEARCH_FAILED_NOT_FOUND,
            **payload_kwargs
        })


class BadUrlFormatHttpException(SearchHTTPException):
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.SEARCH.BAD_URL_FORMAT,
            **payload_kwargs
        })


class ContentUnavailableHttpException(SearchHTTPException):
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.SEARCH.UNAVAILABLE_CONTENT,
            **payload_kwargs
        })

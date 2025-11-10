from src.app.main.common import ApplicationResponseDTO
from src.base.state import project_settings
from .base import TranslationHTTPException


class InvalidLanguageHTTPException(TranslationHTTPException):
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.TRANSLATION.INVALID_LANGUAGE,
            **payload_kwargs
        })

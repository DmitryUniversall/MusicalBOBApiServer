from abc import ABC
from http import HTTPStatus

from pydantic import ValidationError

from src.app.main.common.dto import ApplicationResponseDTO
from src.base.state import project_settings
from src.base.utils.collections import DotDict
from .base import GenericApplicationHTTPException


class RouteSpecificHTTPException(GenericApplicationHTTPException, ABC):
    def get_base_status_info(self) -> DotDict:
        return project_settings.APPLICATION_STATUS_CODES.ROUTE_SPECIFIC


class ForbiddenHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.FORBIDDEN)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.FORBIDDEN,
            **payload_kwargs
        })


class AlreadyExistsHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.CONFLICT)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.ALREADY_EXISTS,
            **payload_kwargs
        })


class NotFoundHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.NOT_FOUND)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.NOT_FOUND,
            **payload_kwargs
        })


class BadRequestHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.BAD_REQUEST)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.BAD_REQUEST,
            **payload_kwargs
        })


class UnprocessableEntityHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.UNPROCESSABLE_ENTITY,
            **payload_kwargs
        })


class SchemaValidationHTTPException(UnprocessableEntityHTTPException):
    def __init__(self, validation_error: ValidationError | None = None, **kwargs) -> None:
        self._validation_error: ValidationError | None = validation_error
        super().__init__(**kwargs)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        payload = super().get_default_response_payload(**payload_kwargs)

        if self._validation_error is not None:
            payload.data = {
                "detail": [
                    {"field": e["loc"][-1], "message": e["msg"]} for e in self._validation_error.errors()  # type: ignore
                ]
            }

        return payload


class InternalServerErrorHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        return ApplicationResponseDTO(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.INTERNAL_SERVER_ERROR,
            **payload_kwargs
        })

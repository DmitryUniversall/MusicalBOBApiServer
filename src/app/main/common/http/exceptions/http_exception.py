from typing import Any

from src.app.main.common.dto import ApplicationResponseDTO
from src.base.exceptions import BaseApplicationError


class ApplicationHTTPException[_contentT: Any](BaseApplicationError):
    """
    A custom exception class for handling HTTP errors with a response payload,
    status code, and optional headers.
    """

    def __init__(
            self,
            *,
            payload: ApplicationResponseDTO[_contentT],
            status_code: int,
            headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(payload.message)

        self.payload: ApplicationResponseDTO = payload
        self.headers: dict[str, str] | None = headers
        self.status_code = status_code

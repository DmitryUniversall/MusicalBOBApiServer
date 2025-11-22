from src.app.main.common import RouteSpecificHTTPException, ApplicationResponseDTO


class InvalidAudioSourceToStreamHTTPException(RouteSpecificHTTPException):
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        base = self.get_base_status_info()

        return ApplicationResponseDTO(**{
            "ok": False,
            **base.STREAM_AUDIO_SOURCE_ROUTE.INVALID_AUDIO_SOURCE,
            **payload_kwargs
        })


class FailedToReadOriginalAudioSourceHTTPException(RouteSpecificHTTPException):
    def __init__(self, audio_source_uuid: str, audio_request_status_code: int, **kwargs) -> None:
        super().__init__(**kwargs)

        self.audio_source_uuid = audio_source_uuid
        self.audio_request_status_code = audio_request_status_code

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        base = self.get_base_status_info()

        return ApplicationResponseDTO(**{
            "ok": False,
            "application_status_code": base.STREAM_AUDIO_SOURCE_ROUTE.FAILED_TO_READ_ORIGINAL_AUDIO_SOURCE.application_status_code,
            "message": base.STREAM_AUDIO_SOURCE_ROUTE.FAILED_TO_READ_ORIGINAL_AUDIO_SOURCE.message.format(self.audio_source_uuid, self.audio_request_status_code),
            **payload_kwargs
        })

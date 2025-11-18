from src.app.main.common import RouteSpecificHTTPException, ApplicationResponseDTO


class InvalidAudioSourceToStreamHTTPException(RouteSpecificHTTPException):
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponseDTO:
        base = self.get_base_status_info()

        return ApplicationResponseDTO(**{
            "ok": False,
            **base.STREAM_AUDIO_SOURCE_ROUTE.INVALID_AUDIO_SOURCE,
            **payload_kwargs
        })

from .internal.repositories import YMSearchRepositoryImpl
from .internal.ym_client import CustomYandexMusicClientImpl, CustomYandexMusicClientI
from ..domain.repositories import YMSearchRepositoryI

CustomYandexMusicClientI.bind_implementation(CustomYandexMusicClientImpl)
YMSearchRepositoryI.bind_implementation(YMSearchRepositoryImpl)  # type: ignore

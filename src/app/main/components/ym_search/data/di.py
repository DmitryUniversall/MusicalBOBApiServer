from .internal.repositories import YMSearchRepositoryImpl
from ..domain.repositories import YMSearchRepositoryI

YMSearchRepositoryI.bind_implementation(YMSearchRepositoryImpl)  # type: ignore

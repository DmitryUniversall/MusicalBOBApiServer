from .internal.repositories_impl import TranslationRepositoryImpl
from ..domain import TranslationRepositoryI

TranslationRepositoryI.bind_implementation(TranslationRepositoryImpl)  # type: ignore

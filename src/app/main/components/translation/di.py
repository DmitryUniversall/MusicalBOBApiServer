from .data import di    # type: ignore

from .domain import TranslationServiceI
from .services_impl import TranslationServiceImpl

TranslationServiceI.bind_implementation(TranslationServiceImpl)  # type: ignore

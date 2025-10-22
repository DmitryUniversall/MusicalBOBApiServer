from abc import ABC

from src.app.main.components.common_search.domain.services import AbstractPlatformSearchService
from src.base.utils.interface import InterfaceMeta


class YMSearchServiceI(AbstractPlatformSearchService, ABC, metaclass=InterfaceMeta):
    pass

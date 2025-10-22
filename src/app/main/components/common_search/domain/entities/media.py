from .author import Author
from .search_entitiy import BaseSearchEntity


class Media(BaseSearchEntity):
    authors: list[Author] = []

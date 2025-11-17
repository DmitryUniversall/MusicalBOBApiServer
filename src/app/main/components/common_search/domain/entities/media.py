from .author import Author
from .search_entitiy import SearchEntity


class Media(SearchEntity):
    authors: list[Author] = []

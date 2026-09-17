import re
from typing import Final

from src.base.utils.constants import UUID_REGEX

YM_PUBLIC_HOST: Final[str] = "music.yandex.ru"

# Yandex can change TLD, so the host is matched by shape instead of by a hardcoded list.
# We never request this host, we only read ids out of the path, so being permissive here is safe.
YM_HOST_REGEX: Final[re.Pattern] = re.compile(r"\A(?:www\.)?music\.yandex\.[a-z]{2,4}(?:\.[a-z]{2,3})?\Z")

YM_APP_SCHEMES: Final[frozenset[str]] = frozenset({"yandexmusic", "yandexmusic-open", "musicsdk"})

# Track, album and artist ids are numeric, and so is the `kind` of a user playlist
NUMERIC_ID_REGEX: Final[re.Pattern] = re.compile(r"\A\d+\Z")

# Playlists shared by link come as a bare uuid or with a two-letter source prefix ("lk.", "ps.").
# The prefix is part of the id and must be preserved for the API call.
PLAYLIST_UUID_REGEX: Final[re.Pattern] = re.compile(rf"\A(?:[a-z]{{2}}\.)?{UUID_REGEX}\Z", re.IGNORECASE)

# Path segments that are expected to be followed by a resource id
LINK_SEGMENT_KEYWORDS: Final[frozenset[str]] = frozenset({"album", "track", "artist", "users", "playlists", "label"})

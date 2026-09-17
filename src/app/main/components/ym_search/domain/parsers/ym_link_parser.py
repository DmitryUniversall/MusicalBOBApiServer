import re
from typing import Final, Optional
from urllib.parse import parse_qs

from src.base.utils.regex import UUID_REGEX
from src.base.utils.url import keyword_pairs, url_segments
from ..entities import (
    YMAlbumLink,
    YMArtistLink,
    YMChartLink,
    YMLink,
    YMSearchLink,
    YMSharedPlaylistLink,
    YMTrackLink,
    YMUserPlaylistLink
)
from ..utils import split_ym_url

# Shared playlists come as a bare uuid or with a two-letter source prefix ("lk.", "ps.").
# The prefix is part of the id and must be preserved for the API call.
_PLAYLIST_UUID_REGEX: Final[re.Pattern] = re.compile(rf"\A(?:[a-z]{{2}}\.)?{UUID_REGEX}\Z", re.IGNORECASE)
_ID_REGEX: Final[re.Pattern] = re.compile(r"\A\d+\Z")

_SEGMENT_KEYWORDS: Final[frozenset[str]] = frozenset({"album", "track", "artist", "users", "playlists", "label"})


def _parse_embed(fragment: str) -> Optional[YMLink]:
    """
    Parses embed/legacy hashbang links: `/iframe/#track/<track_id>/<album_id>`.

    Note the reversed order compared to the page url `/album/<album_id>/track/<track_id>`.

    :param fragment: `str`
        Url fragment without the leading `#`.

    :return: `YMLink | None`
        Parsed link or `None` if the fragment is not a known embed shape.
    """

    segments = url_segments(fragment.lstrip("!"))

    match [segment.lower() for segment in segments]:
        case ["track", track_id, album_id] if _ID_REGEX.match(track_id) and _ID_REGEX.match(album_id):
            return YMTrackLink(track_id=track_id, album_id=album_id)
        case ["track", track_id] if _ID_REGEX.match(track_id):
            return YMTrackLink(track_id=track_id)
        case ["album", album_id] if _ID_REGEX.match(album_id):
            return YMAlbumLink(album_id=album_id)
        case ["artist", artist_id] if _ID_REGEX.match(artist_id):
            return YMArtistLink(artist_id=artist_id)
        case ["playlist", _, kind] if _ID_REGEX.match(kind):
            return YMUserPlaylistLink(owner=segments[1], kind=kind)

    return None


def _parse_playlist(playlist_id: str, owner: Optional[str]) -> Optional[YMLink]:
    if owner is not None and _ID_REGEX.match(playlist_id):
        return YMUserPlaylistLink(owner=owner, kind=playlist_id)
    if _PLAYLIST_UUID_REGEX.match(playlist_id):
        return YMSharedPlaylistLink(playlist_uuid=playlist_id)

    return None


def parse_ym_link(url: str) -> Optional[YMLink]:
    """
    Parses any Yandex Music url into a resource reference.

    :param url: `str`
        Raw user input. Scheme, `www.`, casing, query, fragment, percent-encoding,
        invisible characters and trailing slashes are all tolerated.

    :return: `YMLink | None`
        Parsed reference, or `None` if this is not a recognizable Yandex Music link.
    """

    parts = split_ym_url(url)

    if parts is None:
        return None

    segments = url_segments(parts.path)
    lowered = [segment.lower() for segment in segments]

    if parts.fragment and (not segments or lowered[0] == "iframe"):
        return _parse_embed(parts.fragment)

    pairs = keyword_pairs(segments, _SEGMENT_KEYWORDS)

    if (track_id := pairs.get("track")) is not None and _ID_REGEX.match(track_id):
        album_id = pairs.get("album")
        return YMTrackLink(
            track_id=track_id,
            album_id=album_id if album_id is not None and _ID_REGEX.match(album_id) else None
        )

    if (album_id := pairs.get("album")) is not None and _ID_REGEX.match(album_id):
        return YMAlbumLink(album_id=album_id)

    if (playlist_id := pairs.get("playlists")) is not None:
        return _parse_playlist(playlist_id, pairs.get("users"))

    if (artist_id := pairs.get("artist")) is not None and _ID_REGEX.match(artist_id):
        return YMArtistLink(artist_id=artist_id)

    if lowered[:1] == ["chart"]:
        return YMChartLink(region=segments[1] if len(segments) > 1 else None)

    if lowered[:1] == ["search"] and (text := parse_qs(parts.query).get("text")):
        return YMSearchLink(query=text[0])

    return None

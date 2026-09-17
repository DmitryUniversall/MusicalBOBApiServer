import re
from dataclasses import dataclass
from typing import Final, Optional
from urllib.parse import parse_qs, unquote, urlsplit

from src.base.utils.regex import UUID_REGEX

YM_PUBLIC_HOST: Final[str] = "music.yandex.ru"

# Yandex renames TLDs regularly (ru -> com, com.tr, ...), so the host is matched by shape
# instead of by a hardcoded list. We never request this host, we only read ids out of the
# path, so being permissive here is safe.
_YM_HOST_REGEX: Final[re.Pattern] = re.compile(r"\A(?:www\.)?music\.yandex\.[a-z]{2,4}(?:\.[a-z]{2,3})?\Z")
_YM_APP_SCHEMES: Final[frozenset[str]] = frozenset({"yandexmusic", "yandexmusic-open", "musicsdk"})
_HTTP_SCHEMES: Final[frozenset[str]] = frozenset({"http", "https"})

# Shared playlists come as a bare uuid or with a two-letter source prefix ("lk.", "ps.").
# The prefix is part of the id and must be preserved for the API call.
_PLAYLIST_UUID_REGEX: Final[re.Pattern] = re.compile(rf"\A(?:[a-z]{{2}}\.)?{UUID_REGEX}\Z", re.IGNORECASE)
_ID_REGEX: Final[re.Pattern] = re.compile(r"\A\d+\Z")
_SCHEME_REGEX: Final[re.Pattern] = re.compile(r"\A[a-z][a-z0-9+.\-]*://", re.IGNORECASE)
_INVISIBLE_REGEX: Final[re.Pattern] = re.compile(r"[​-‏‪-‮⁦-⁩﻿]")

_SEGMENT_KEYWORDS: Final[frozenset[str]] = frozenset({"album", "track", "artist", "users", "playlists", "label"})


def canonical_track_url(track_id: str | int) -> str:
    return f"https://{YM_PUBLIC_HOST}/track/{track_id}"


def canonical_album_url(album_id: str | int) -> str:
    return f"https://{YM_PUBLIC_HOST}/album/{album_id}"


def canonical_artist_url(artist_id: str | int) -> str:
    return f"https://{YM_PUBLIC_HOST}/artist/{artist_id}"


def canonical_user_url(login: str) -> str:
    return f"https://{YM_PUBLIC_HOST}/users/{login}"


def canonical_user_playlist_url(owner: str, kind: str | int) -> str:
    return f"https://{YM_PUBLIC_HOST}/users/{owner}/playlists/{kind}"


def canonical_shared_playlist_url(playlist_uuid: str) -> str:
    return f"https://{YM_PUBLIC_HOST}/playlists/{playlist_uuid}"


def canonical_chart_url(region: Optional[str] = None) -> str:
    return f"https://{YM_PUBLIC_HOST}/chart" + (f"/{region}" if region is not None else "")


@dataclass(frozen=True, slots=True)
class YMTrackLink:
    track_id: str
    album_id: Optional[str] = None  # Album is only a context hint, track_id alone identifies the track

    @property
    def canonical_url(self) -> str:
        return canonical_track_url(self.track_id)


@dataclass(frozen=True, slots=True)
class YMAlbumLink:
    album_id: str

    @property
    def canonical_url(self) -> str:
        return canonical_album_url(self.album_id)


@dataclass(frozen=True, slots=True)
class YMUserPlaylistLink:
    owner: str
    kind: str

    @property
    def canonical_url(self) -> str:
        return canonical_user_playlist_url(self.owner, self.kind)


@dataclass(frozen=True, slots=True)
class YMSharedPlaylistLink:
    playlist_uuid: str  # May carry a "lk."/"ps." prefix

    @property
    def canonical_url(self) -> str:
        return canonical_shared_playlist_url(self.playlist_uuid)


@dataclass(frozen=True, slots=True)
class YMArtistLink:
    artist_id: str

    @property
    def canonical_url(self) -> str:
        return canonical_artist_url(self.artist_id)


@dataclass(frozen=True, slots=True)
class YMChartLink:
    region: Optional[str] = None

    @property
    def canonical_url(self) -> str:
        return canonical_chart_url(self.region)


@dataclass(frozen=True, slots=True)
class YMSearchLink:
    query: str

    @property
    def canonical_url(self) -> str:
        return f"https://{YM_PUBLIC_HOST}/search?text={self.query}"


type YMPlaylistLink = YMUserPlaylistLink | YMSharedPlaylistLink

type YMLink = (
    YMTrackLink
    | YMAlbumLink
    | YMUserPlaylistLink
    | YMSharedPlaylistLink
    | YMArtistLink
    | YMChartLink
    | YMSearchLink
)


def _normalize(raw: str) -> str:
    text = _INVISIBLE_REGEX.sub("", raw).strip().strip("<>\"'")
    return text if _SCHEME_REGEX.match(text) else f"https://{text}"


def _segments(path: str) -> list[str]:
    return [unquote(segment) for segment in path.split("/") if segment]


def _keyword_pairs(segments: list[str]) -> dict[str, str]:
    """
    Collects `<keyword>/<value>` pairs anywhere in the path.

    Position-independent on purpose: an added locale prefix (`/ru/album/1`) or a trailing
    tab (`/artist/1/tracks`) must not break resolution.

    :param segments: `list[str]`
        Decoded path segments.

    :return: `dict[str, str]`
        Mapping of keyword to the segment following it (first occurrence wins).
    """

    pairs: dict[str, str] = {}

    index = 0
    while index < len(segments) - 1:
        keyword = segments[index].lower()

        if keyword in _SEGMENT_KEYWORDS and keyword not in pairs:
            pairs[keyword] = segments[index + 1]
            index += 2
        else:
            index += 1

    return pairs


def _parse_embed(fragment: str) -> Optional[YMLink]:
    """
    Parses embed/legacy hashbang links: `/iframe/#track/<track_id>/<album_id>`.

    Note the reversed order compared to the page url `/album/<album_id>/track/<track_id>`.

    :param fragment: `str`
        Url fragment without the leading `#`.

    :return: `YMLink | None`
        Parsed link or `None` if the fragment is not a known embed shape.
    """

    segments = _segments(fragment.lstrip("!"))

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


def is_ym_url(url: str) -> bool:
    """
    Checks whether `url` points to Yandex Music, regardless of the resource it points to.

    :param url: `str`
        Raw user input.

    :return: `bool`
        `True` if the host (or the app scheme) belongs to Yandex Music.
    """

    parts = urlsplit(_normalize(url))
    scheme = parts.scheme.lower()

    if scheme in _YM_APP_SCHEMES:
        return True

    return scheme in _HTTP_SCHEMES and _YM_HOST_REGEX.match(parts.hostname or "") is not None


def parse_ym_link(url: str) -> Optional[YMLink]:
    """
    Parses any Yandex Music url into a resource reference.

    :param url: `str`
        Raw user input. Scheme, `www.`, casing, query, fragment, percent-encoding,
        invisible characters and trailing slashes are all tolerated.

    :return: `YMLink | None`
        Parsed reference, or `None` if this is not a recognizable Yandex Music link.
    """

    parts = urlsplit(_normalize(url))
    scheme = parts.scheme.lower()

    if scheme in _YM_APP_SCHEMES:  # yandexmusic://album/123/track/456 -> netloc holds the first segment
        path = f"/{parts.netloc}{parts.path}"
    elif scheme in _HTTP_SCHEMES and _YM_HOST_REGEX.match(parts.hostname or ""):
        path = parts.path
    else:
        return None

    segments = _segments(path)
    lowered = [segment.lower() for segment in segments]

    if parts.fragment and (not segments or lowered[0] == "iframe"):
        return _parse_embed(parts.fragment)

    pairs = _keyword_pairs(segments)

    if (track_id := pairs.get("track")) is not None and _ID_REGEX.match(track_id):
        album_id = pairs.get("album")
        return YMTrackLink(
            track_id=track_id,
            album_id=album_id if album_id is not None and _ID_REGEX.match(album_id) else None
        )

    if (album_id := pairs.get("album")) is not None and _ID_REGEX.match(album_id):
        return YMAlbumLink(album_id=album_id)

    if (playlist_id := pairs.get("playlists")) is not None:
        owner = pairs.get("users")

        if owner is not None and _ID_REGEX.match(playlist_id):
            return YMUserPlaylistLink(owner=owner, kind=playlist_id)
        if _PLAYLIST_UUID_REGEX.match(playlist_id):
            return YMSharedPlaylistLink(playlist_uuid=playlist_id)

        return None

    if (artist_id := pairs.get("artist")) is not None and _ID_REGEX.match(artist_id):
        return YMArtistLink(artist_id=artist_id)

    if lowered[:1] == ["chart"]:
        return YMChartLink(region=segments[1] if len(segments) > 1 else None)

    if lowered[:1] == ["search"] and (text := parse_qs(parts.query).get("text")):
        return YMSearchLink(query=text[0])

    return None

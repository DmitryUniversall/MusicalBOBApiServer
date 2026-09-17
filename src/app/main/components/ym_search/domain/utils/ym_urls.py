from typing import Optional
from urllib.parse import SplitResult, quote, urlsplit

from src.base.utils.constants import HTTP_SCHEMES
from src.base.utils.url import normalize_url
from ..constants import YM_APP_SCHEMES, YM_HOST_REGEX, YM_PUBLIC_HOST


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


def canonical_search_url(query: str) -> str:
    return f"https://{YM_PUBLIC_HOST}/search?text={quote(query)}"


def split_ym_url(url: str) -> Optional[SplitResult]:
    """
    Normalizes `url` and splits it, if it belongs to Yandex Music.

    The host is compared after `urlsplit`, not by prefix: `hostname` drops the port and
    the userinfo part, so neither `music.yandex.ru.evil.com` nor `music.yandex.ru@evil.com`
    can pass as Yandex Music.

    :param url: `str`
        Raw user input.

    :return: `SplitResult | None`
        Split url, or `None` if the url does not belong to Yandex Music.
    """

    parts = urlsplit(normalize_url(url))
    scheme = parts.scheme.lower()

    if scheme in YM_APP_SCHEMES:  # yandexmusic://album/123/track/456 -> netloc holds the first segment
        return parts._replace(netloc="", path=f"/{parts.netloc}{parts.path}")
    if scheme in HTTP_SCHEMES and YM_HOST_REGEX.match(parts.hostname or ""):
        return parts

    return None


def is_ym_url(url: str) -> bool:
    """
    Checks whether `url` points to Yandex Music, regardless of the resource it points to.

    :param url: `str`
        Raw user input.

    :return: `bool`
        `True` if the host (or the app scheme) belongs to Yandex Music.
    """

    return split_ym_url(url) is not None

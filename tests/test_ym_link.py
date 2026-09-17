from typing import Optional

import pytest

from src.app.main.components.ym_search.domain.entities import (
    YMAlbumLink,
    YMArtistLink,
    YMChartLink,
    YMLink,
    YMSearchLink,
    YMSharedPlaylistLink,
    YMTrackLink,
    YMUserPlaylistLink,
    is_ym_url,
    parse_ym_link
)

UUID = "1f2e3d4c-5b6a-7980-9a8b-7c6d5e4f3a2b"


@pytest.mark.parametrize("url, expected", [
    # Tracks
    ("https://music.yandex.ru/album/540508/track/4878838", YMTrackLink("4878838", "540508")),
    ("https://music.yandex.com/album/540508/track/4878838", YMTrackLink("4878838", "540508")),
    ("http://music.yandex.kz/album/540508/track/4878838/", YMTrackLink("4878838", "540508")),
    ("https://music.yandex.com.tr/album/1/track/2", YMTrackLink("2", "1")),
    ("music.yandex.ru/album/1/track/2", YMTrackLink("2", "1")),
    ("https://www.music.yandex.ru/album/1/track/2", YMTrackLink("2", "1")),
    ("HTTPS://MUSIC.YANDEX.RU/ALBUM/1/TRACK/2", YMTrackLink("2", "1")),
    ("https://music.yandex.ru/track/4878838", YMTrackLink("4878838", None)),
    ("  https://music.yandex.ru/track/4878838/  ", YMTrackLink("4878838", None)),
    ("​https://music.yandex.ru/track/4878838​", YMTrackLink("4878838", None)),
    ("https://music.yandex.ru/album/1/track/2?utm_source=android&utm_medium=copy_link", YMTrackLink("2", "1")),
    ("https://music.yandex.ru/album/1/track/2?activeTab=track-list&dir=desc", YMTrackLink("2", "1")),
    ("https://music.yandex.ru/album/1/track/2/lyrics", YMTrackLink("2", "1")),
    ("https://music.yandex.ru//album//1//track//2", YMTrackLink("2", "1")),
    ("https://music.yandex.ru/ru/album/1/track/2", YMTrackLink("2", "1")),  # Hypothetical locale prefix
    ("yandexmusic://album/1/track/2", YMTrackLink("2", "1")),
    ("https://music.yandex.ru/iframe/#track/19523692/4297694", YMTrackLink("19523692", "4297694")),  # Reversed order
    ("https://music.yandex.ru/#!/track/123/456", YMTrackLink("123", "456")),
    # Albums
    ("https://music.yandex.ru/album/3840501", YMAlbumLink("3840501")),
    ("https://music.yandex.by/album/3840501/", YMAlbumLink("3840501")),
    ("https://music.yandex.ru/album/3840501?activeTab=about", YMAlbumLink("3840501")),
    ("https://music.yandex.ru/iframe/#album/3840501", YMAlbumLink("3840501")),
    # User playlists
    ("https://music.yandex.ru/users/music.partners/playlists/1245", YMUserPlaylistLink("music.partners", "1245")),
    ("https://music.yandex.ru/users/ya.playlist/playlists/1036/", YMUserPlaylistLink("ya.playlist", "1036")),
    ("https://music.yandex.ru/users/vasya%40yandex.ru/playlists/3", YMUserPlaylistLink("vasya@yandex.ru", "3")),
    ("https://music.yandex.ru/users/some%20user/playlists/3", YMUserPlaylistLink("some user", "3")),
    ("https://music.yandex.ru/iframe/#playlist/music.partners/1245", YMUserPlaylistLink("music.partners", "1245")),
    # Playlists shared by link
    (f"https://music.yandex.ru/playlists/{UUID}", YMSharedPlaylistLink(UUID)),
    (f"https://music.yandex.ru/playlists/lk.{UUID}", YMSharedPlaylistLink(f"lk.{UUID}")),
    (f"https://music.yandex.com/playlists/ps.{UUID}?utm_medium=copy_link", YMSharedPlaylistLink(f"ps.{UUID}")),
    (f"https://music.yandex.ru/playlists/{UUID.upper()}", YMSharedPlaylistLink(UUID.upper())),
    # Artist, chart, search
    ("https://music.yandex.ru/artist/617526", YMArtistLink("617526")),
    ("https://music.yandex.ru/artist/617526/tracks", YMArtistLink("617526")),
    ("https://music.yandex.ru/chart", YMChartLink(None)),
    ("https://music.yandex.ru/chart/world", YMChartLink("world")),
    ("https://music.yandex.ru/search?text=nirvana%20come%20as%20you%20are", YMSearchLink("nirvana come as you are")),
    # Must be rejected
    ("https://music.yandex.ru.evil.com/track/1", None),
    ("https://music.yandex.ru@evil.com/track/1", None),
    ("https://evil.com/music.yandex.ru/track/1", None),
    ("https://music.youtube.com/watch?v=1", None),
    ("https://music.yandex.ru/", None),
    ("https://music.yandex.ru/home", None),
    ("https://music.yandex.ru/playlists/not-a-uuid", None),
    ("https://music.yandex.ru/album/abc/track/def", None),
    ("just some text", None),
    ("", None),
])
def test_parse_ym_link(url: str, expected: Optional[YMLink]) -> None:
    assert parse_ym_link(url) == expected


@pytest.mark.parametrize("url, expected", [
    ("https://music.yandex.ru/home", True),
    ("music.yandex.com/album/1", True),
    ("yandexmusic://album/1/track/2", True),
    ("https://music.yandex.ru.evil.com/track/1", False),
    ("https://music.yandex.ru@evil.com/track/1", False),
    ("nirvana come as you are", False),
])
def test_is_ym_url(url: str, expected: bool) -> None:
    assert is_ym_url(url) is expected


@pytest.mark.parametrize("url, canonical", [
    ("https://music.yandex.com/album/540508/track/4878838?utm_medium=copy_link", "https://music.yandex.ru/track/4878838"),
    ("https://music.yandex.ru/track/4878838/", "https://music.yandex.ru/track/4878838"),
    ("https://music.yandex.ru/iframe/#track/4878838/540508", "https://music.yandex.ru/track/4878838"),
    ("https://music.yandex.by/album/3840501/", "https://music.yandex.ru/album/3840501"),
    (f"https://music.yandex.com/playlists/lk.{UUID}?x=1", f"https://music.yandex.ru/playlists/lk.{UUID}"),
])
def test_canonical_url_is_stable_across_link_shapes(url: str, canonical: str) -> None:
    link = parse_ym_link(url)

    assert link is not None
    assert link.canonical_url == canonical

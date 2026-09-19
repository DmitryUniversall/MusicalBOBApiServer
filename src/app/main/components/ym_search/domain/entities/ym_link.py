from dataclasses import dataclass
from typing import Optional

from ..utils import (
    canonical_album_url,
    canonical_artist_url,
    canonical_chart_url,
    canonical_search_url,
    canonical_shared_playlist_url,
    canonical_track_url,
    canonical_user_playlist_url
)


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
        return canonical_search_url(self.query)


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

import logging
from typing import Optional, Iterable

import yandex_music

from src.app.main.components.audio_sources import AudioSourceServiceI, AudioSource
from src.app.main.components.common_search import Author, SearchPlatform, Playlist, Track, Lyrics
from src.app.main.components.common_search.domain.exceptions import BadUrlFormatHttpException, SearchFailedNotFoundHttpException
from src.app.main.components.search_cache import SearchCacheServiceI
from src.app.main.components.ym_search.domain.entities import (
    YMAlbumLink,
    YMPlaylistLink,
    YMTrackLink,
    YMUserPlaylistLink
)
from src.app.main.components.ym_search.domain.parsers import parse_ym_link
from src.app.main.components.ym_search.domain.utils import (
    canonical_artist_url,
    canonical_shared_playlist_url,
    canonical_track_url,
    canonical_user_playlist_url,
    canonical_user_url
)
from src.app.main.components.ym_search.domain.repositories import YMSearchRepositoryI
from src.base.state import project_settings
from src.base.utils.async_tools import gather_for_each
from src.base.utils.cache import CacheContainer
from ..ym_client import CustomAsyncYMClientI

_logger = logging.getLogger(__name__)


class YMSearchRepositoryImpl(YMSearchRepositoryI):
    def __init__(
            self,
            _ym_client: CustomAsyncYMClientI,
            _audio_source_service: AudioSourceServiceI,
            _search_cache_service: SearchCacheServiceI,
    ) -> None:
        self._ym_client = _ym_client
        self._audio_source_service = _audio_source_service
        self._search_cache_service = _search_cache_service

        self._lyrics_cache: CacheContainer[str, Lyrics] = CacheContainer(default_ttl=project_settings.YM_CACHE_EXPIRE)  # TODO: Use search cache service

    async def _ym_artist_to_author(self, artist: yandex_music.Artist, **kwargs) -> 'Author':
        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": canonical_artist_url(artist.id),
            "image_source": artist.op_image,
            "title": artist.name,
            **kwargs
        }

        return Author(**data)

    async def _ym_user_to_author(self, user: yandex_music.User, **kwargs) -> 'Author':
        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": canonical_user_url(user.login),
            "image_source": canonical_user_url(user.login),
            "title": user.name,
            **kwargs
        }

        return Author(**data)

    async def _ym_album_to_playlist(
            self,
            album: yandex_music.Album,
            source: str,
            tracks: Optional[Iterable[yandex_music.Track]] = None,
            **kwargs
    ) -> Playlist:
        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": source,
            "image_source": f'https://{album.cover_uri.replace("%%", "400x300")}' if album.cover_uri is not None else None,
            "title": album.title,
            "authors": list(await gather_for_each(self._ym_artist_to_author, album.artists)),
            **kwargs
        }

        playlist = Playlist(**data)

        if tracks is not None:
            playlist.extend(tracks=await gather_for_each(self._ym_track_to_track, tracks))

        return playlist

    async def _ym_playlist_to_playlist(
            self,
            playlist: yandex_music.Playlist,
            source: str,
            tracks: Optional[Iterable[yandex_music.Track]] = None,
            **kwargs
    ) -> Playlist:
        owner = playlist.owner  # Playlists shared by link may come without an owner
        cover_uri = playlist.cover.uri if playlist.cover is not None else None

        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": source,
            "image_source": f'https://{cover_uri.replace("%%", "400x400")}' if cover_uri is not None else None,
            "title": playlist.title,
            "authors": [await self._ym_user_to_author(owner)] if owner is not None else [],
            **kwargs
        }

        result = Playlist(**data)

        if tracks is not None:
            result.extend(tracks=await gather_for_each(self._ym_track_to_track, tracks))

        return result

    async def _ym_track_to_track(self, track: yandex_music.Track, **kwargs) -> Track:
        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": canonical_track_url(track.id),
            "title": track.title,
            "image_source": f'https://{track.cover_uri.replace("%%", "400x300")}' if track.cover_uri is not None else None,
            "authors": list(await gather_for_each(self._ym_artist_to_author, track.artists)),
            "duration": track.duration_ms,
            "raw": track,
            **kwargs
        }

        return Track(**data)

    @staticmethod
    def _track_link_from_source(source: str) -> YMTrackLink:
        link = parse_ym_link(source)

        if not isinstance(link, YMTrackLink):
            raise BadUrlFormatHttpException(message=f"Track source '{source}' is not a yandex music track url")

        return link

    async def _fetch_track(self, link: YMTrackLink) -> Track:
        track = await self._ym_client.get_track(track_id=link.track_id, album_id=link.album_id)
        return await self._ym_track_to_track(track=track)

    async def _get_cached_track(self, link: YMTrackLink) -> Optional[Track]:
        return await self._search_cache_service.get_cached_track_by_source(source=link.canonical_url)

    async def get_track(self, link: YMTrackLink) -> Track:
        if (cached_track := await self._get_cached_track(link)) is not None:
            _logger.debug(f"Found cached track for link: {link}")
            return cached_track

        fetched_track = await self._fetch_track(link)
        await self._search_cache_service.cache_search_entity(fetched_track)

        return fetched_track

    async def _fetch_playlist(self, link: YMPlaylistLink) -> Playlist:
        if isinstance(link, YMUserPlaylistLink):
            playlist, tracks = await self._ym_client.get_playlist(username=link.owner, playlist_id=link.kind)
        else:
            playlist, tracks = await self._ym_client.get_playlist_by_uuid(playlist_uuid=link.playlist_uuid)

        return await self._ym_playlist_to_playlist(playlist=playlist, tracks=tracks, source=self._playlist_source(playlist, link))

    @staticmethod
    def _playlist_source(playlist: yandex_music.Playlist, link: YMPlaylistLink) -> str:
        # A playlist opened by a shared link is the same entity as the one opened from its
        # owner's page, so both must end up under the same cache key
        if playlist.owner is not None and playlist.kind is not None:
            return canonical_user_playlist_url(playlist.owner.login, playlist.kind)
        if playlist.playlist_uuid is not None:
            return canonical_shared_playlist_url(playlist.playlist_uuid)

        return link.canonical_url

    async def _get_cached_playlist(self, _: YMPlaylistLink) -> Optional[Playlist]:  # TODO: Get playlist meta from cache and load only tracks
        return None  # We don't cache playlists because its content can be changed

    async def get_playlist(self, link: YMPlaylistLink) -> Playlist:
        if (cached_playlist := await self._get_cached_playlist(link)) is not None:
            _logger.debug(f"Found cached playlist for link: {link}")
            return cached_playlist

        fetched_playlist = await self._fetch_playlist(link)
        # await self._search_cache_service.cache_search_entity(fetched_playlist)  # We don't cache playlists because its content can be changed

        return fetched_playlist

    async def _fetch_album(self, link: YMAlbumLink) -> Playlist:
        album, tracks = await self._ym_client.get_album_with_tracks(album_id=link.album_id)
        return await self._ym_album_to_playlist(album=album, tracks=tracks, source=link.canonical_url)

    async def _get_cached_album(self, link: YMAlbumLink) -> Optional[Playlist]:  # Caching album is not fully safe, but I'll do it anyway
        return await self._search_cache_service.get_cached_playlist_by_source(source=link.canonical_url)

    async def get_album(self, link: YMAlbumLink) -> Playlist:
        if (cached_album := await self._get_cached_album(link)) is not None:
            _logger.debug(f"Found cached album for link: {link}")
            return cached_album

        fetched_album = await self._fetch_album(link)
        await self._search_cache_service.cache_search_entity(fetched_album)  # Caching album is not fully safe, but I'll do it anyway

        return fetched_album

    async def _fetch_audio_sources(self, link: YMTrackLink) -> tuple[AudioSource, ...]:
        raw = await self._ym_client.get_track(track_id=link.track_id, album_id=link.album_id)
        return await self._get_audio_sources_for_raw_track(raw=raw)

    async def _get_cached_audio_sources_by_track_url(self, track_source: str) -> tuple[AudioSource, ...]:  # Caching album is not fully safe, but I'll do it anyway
        return await self._audio_source_service.get_cached_audio_sources_for_track(track_source)

    async def get_audio_sources_for_link(self, link: YMTrackLink) -> tuple[AudioSource, ...]:
        if cached_audio_sources := await self._get_cached_audio_sources_by_track_url(link.canonical_url):
            _logger.debug(f"Found cached audio sources for link: {link}")
            return cached_audio_sources

        fetched_audio_sources = await self._fetch_audio_sources(link)
        await self._audio_source_service.cache_audio_sources_and_map_with_track(link.canonical_url, fetched_audio_sources)

        return fetched_audio_sources

    async def _get_audio_sources_for_raw_track(self, raw: yandex_music.Track) -> tuple[AudioSource, ...]:
        return tuple(map(
            lambda it: AudioSource(source=it),
            await self._ym_client.get_audio_sources_by_raw(raw=raw)
        ))

    async def get_audio_sources_for_track(self, track: Track) -> tuple[AudioSource, ...]:
        if cached_audio_sources := await self._get_cached_audio_sources_by_track_url(track.source):
            _logger.debug(f"Found cached audio sources for track: {track.source}")
            return cached_audio_sources

        if track.raw is not None and isinstance(track.raw, yandex_music.Track):
            sources = await self._get_audio_sources_for_raw_track(raw=track.raw)
        else:
            sources = await self._fetch_audio_sources(self._track_link_from_source(track.source))

        await self._audio_source_service.cache_audio_sources_and_map_with_track(track.source, sources)

        return sources

    async def _fetch_lyrics(self, link: YMTrackLink) -> Lyrics:
        raw = await self._ym_client.get_track(track_id=link.track_id, album_id=link.album_id)
        return await self._get_lyrics_for_raw_track(raw=raw)

    async def _get_cached_lyrics_by_url(self, url: str) -> Optional[Lyrics]:
        return self._lyrics_cache.get(url, None)

    async def get_lyrics_for_link(self, link: YMTrackLink) -> Lyrics:
        if (cached_lyrics := await self._get_cached_lyrics_by_url(link.canonical_url)) is not None:
            _logger.debug(f"Found cached lyrics for link: {link}")
            return cached_lyrics

        fetched_lyrics = await self._fetch_lyrics(link)
        self._lyrics_cache.set(link.canonical_url, fetched_lyrics)

        return fetched_lyrics

    async def _get_lyrics_for_raw_track(self, raw: yandex_music.Track) -> Lyrics:
        return Lyrics(lyrics=await self._ym_client.get_lyrics_by_raw(raw=raw))

    async def get_lyrics_for_track(self, track: Track) -> Lyrics:
        if (cached_lyrics := await self._get_cached_lyrics_by_url(url=track.source)) is not None:
            _logger.debug(f"Found cached lyrics for track: {track.source}")
            return cached_lyrics

        if track.raw is not None and isinstance(track.raw, yandex_music.Track):
            fetched_lyrics = await self._get_lyrics_for_raw_track(track.raw)
        else:
            fetched_lyrics = await self._fetch_lyrics(self._track_link_from_source(track.source))

        self._lyrics_cache.set(track.source, fetched_lyrics)

        return fetched_lyrics

    async def search_track_by_name(self, query: str) -> Track:
        tracks = await gather_for_each(self._ym_track_to_track, await self._ym_client.search_track_by_name(query))

        if not tracks:
            raise SearchFailedNotFoundHttpException()

        best_match_track = tracks[0]
        best_match_track.variations = list(tracks[1:])

        return best_match_track

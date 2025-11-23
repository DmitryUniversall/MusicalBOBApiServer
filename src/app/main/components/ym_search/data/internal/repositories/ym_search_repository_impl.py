import logging
from typing import Optional, Iterable

import yandex_music

from src.app.main.components.audio_sources import AudioSourceServiceI, AudioSource
from src.app.main.components.common_search import Author, SearchPlatform, Playlist, Track, Lyrics
from src.app.main.components.common_search.domain.exceptions import SearchFailedNotFoundHttpException
from src.app.main.components.search_cache import SearchCacheServiceI
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
            "source": f"https://music.yandex.ru/artist/{artist.id}",
            "image_source": artist.op_image,
            "title": artist.name,
            **kwargs
        }

        return Author(**data)

    async def _ym_user_to_author(self, user: yandex_music.User, **kwargs) -> 'Author':
        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": f"https://music.yandex.ru/users/{user.login}/",
            "image_source": f"https://music.yandex.ru/users/{user.login}/",
            "title": user.name,
            **kwargs
        }

        return Author(**data)

    async def _ym_album_to_playlist(
            self,
            album: yandex_music.Album,
            tracks: Optional[Iterable[yandex_music.Track]] = None,
            **kwargs
    ) -> Playlist:
        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": f"https://music.yandex.ru/album/{album.id}",
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
            tracks: Optional[Iterable[yandex_music.Track]] = None,
            **kwargs
    ) -> Playlist:
        if playlist.owner is None:
            raise

        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": f"https://music.yandex.ru/users/{playlist.owner.login}/playlists/{playlist.kind}",
            "image_source": f'https://{playlist.cover.uri.replace("%%", "400x400")}' if playlist.cover.uri is not None else None,
            "title": playlist.title,
            "authors": [await self._ym_user_to_author(playlist.owner)],
            **kwargs
        }

        playlist = Playlist(**data)

        if tracks is not None:
            playlist.extend(tracks=await gather_for_each(self._ym_track_to_track, tracks))

        return playlist

    async def _ym_track_to_track(self, track: yandex_music.Track, **kwargs) -> Track:
        data = {
            "platform": SearchPlatform.YANDEX_MUSIC,
            "source": f"https://music.yandex.ru/track/{track.id}/",
            "title": track.title,
            "image_source": f'https://{track.cover_uri.replace("%%", "400x300")}' if track.cover_uri is not None else None,
            "authors": list(await gather_for_each(self._ym_artist_to_author, track.artists)),
            "duration": track.duration_ms,
            "raw": track,
            **kwargs
        }

        return Track(**data)

    async def _fetch_track_by_url(self, url: str) -> Track:
        track = await self._ym_client.get_track_by_url(url=url)
        return await self._ym_track_to_track(track=track, source=url)

    async def _get_cached_track_by_url(self, url: str) -> Optional[Track]:
        return await self._search_cache_service.get_cached_track_by_source(source=url)

    async def get_track_by_url(self, url: str) -> Track:
        if (cached_track := await self._get_cached_track_by_url(url)) is not None:
            _logger.debug(f"Found cached track for url: {url}")
            return cached_track

        fetched_track = await self._fetch_track_by_url(url)
        await self._search_cache_service.cache_search_entity(fetched_track)

        return fetched_track

    async def _fetch_playlist_by_url(self, url: str) -> Playlist:
        playlist, tracks = await self._ym_client.get_playlist_with_tracks_by_url(url=url)
        return await self._ym_playlist_to_playlist(playlist=playlist, tracks=tracks, source=url)

    async def _get_cached_playlist_by_url(self, _: str) -> Optional[Playlist]:  # TODO: Get playlist meta from cache and load only tracks
        return None  # We don't cache playlists because its content can be changed

    async def get_playlist_by_url(self, url: str) -> Playlist:
        if (cached_playlist := await self._get_cached_playlist_by_url(url)) is not None:
            _logger.debug(f"Found cached playlist for url: {url}")
            return cached_playlist

        fetched_playlist = await self._fetch_playlist_by_url(url)
        # await self._search_cache_service.cache_search_entity(fetched_playlist)  # We don't cache playlists because its content can be changed

        return fetched_playlist

    async def _fetch_album_by_url(self, url: str) -> Playlist:
        album, tracks = await self._ym_client.get_album_with_tracks_by_url(url=url)
        return await self._ym_album_to_playlist(album=album, tracks=tracks, source=url)

    async def _get_cached_album_by_url(self, url: str) -> Optional[Playlist]:  # Caching album is not fully safe, but I'll do it anyway
        return await self._search_cache_service.get_cached_playlist_by_source(source=url)

    async def get_album_by_url(self, url: str) -> Playlist:
        if (cached_album := await self._get_cached_album_by_url(url)) is not None:
            _logger.debug(f"Found cached album for url: {url}")
            return cached_album

        fetched_album = await self._fetch_album_by_url(url)
        await self._search_cache_service.cache_search_entity(fetched_album)  # Caching album is not fully safe, but I'll do it anyway

        return fetched_album

    async def _fetch_audio_sources_by_url(self, url: str) -> tuple[AudioSource, ...]:
        return tuple(map(
            lambda it: AudioSource(source=it),
            await self._ym_client.get_audio_sources_by_url(url=url)
        ))

    async def _get_cached_audio_sources_by_track_url(self, track_source: str) -> tuple[AudioSource, ...]:  # Caching album is not fully safe, but I'll do it anyway
        return await self._audio_source_service.get_cached_audio_sources_for_track(track_source)

    async def get_audio_sources_by_url(self, url: str) -> tuple[AudioSource, ...]:
        fetched_audio_sources = await self._fetch_audio_sources_by_url(url)
        await self._audio_source_service.cache_audio_sources(fetched_audio_sources)

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
            sources = await self._fetch_audio_sources_by_url(url=track.source)  # Using _fetch_audio_sources_by_url to avoid another cache check

        await self._audio_source_service.cache_audio_sources_and_map_with_track(track.source, sources)

        return sources

    async def _fetch_lyrics_by_url(self, url: str) -> Lyrics:
        return Lyrics(lyrics=await self._ym_client.get_lyrics_by_url(url=url))

    async def _get_cached_lyrics_by_url(self, url: str) -> Optional[Lyrics]:
        return self._lyrics_cache.get(url, None)

    async def get_lyrics_by_url(self, url: str) -> Lyrics:
        if (cached_lyrics := await self._get_cached_lyrics_by_url(url)) is not None:
            _logger.debug(f"Found cached lyrics for url: {url}")
            return cached_lyrics

        fetched_lyrics = await self._fetch_lyrics_by_url(url)
        self._lyrics_cache.set(url, fetched_lyrics)

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
            fetched_lyrics = await self._fetch_lyrics_by_url(url=track.source)  # Using _fetch_lyrics_by_url to avoid another cache check

        self._lyrics_cache.set(track.source, fetched_lyrics)

        return fetched_lyrics

    async def search_track_by_name(self, query: str) -> Track:
        tracks = await gather_for_each(self._ym_track_to_track, await self._ym_client.search_track_by_name(query))

        if not tracks:
            raise SearchFailedNotFoundHttpException()

        best_match_track = tracks[0]
        best_match_track.variations = list(tracks[1:])

        return best_match_track

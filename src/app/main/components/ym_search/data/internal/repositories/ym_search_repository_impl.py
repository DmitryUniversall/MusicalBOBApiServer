from typing import Optional, Iterable

import yandex_music

from src.app.main.components.common_search import Author, SearchPlatform, Playlist, Track, AudioSource
from src.app.main.components.ym_search.domain.repositories import YMSearchRepositoryI
from src.base.utils.async_tools import gather_for_each
from ..ym_client import CustomYandexMusicClientI


class YMSearchRepositoryImpl(YMSearchRepositoryI):
    def __init__(self) -> None:
        self._ym_client: CustomYandexMusicClientI = CustomYandexMusicClientI.get_implementation()

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

    def _wrap_with_audio_source(self, sources: Iterable[str]) -> tuple[AudioSource, ...]:
        return tuple(AudioSource(source=source) for source in sources)

    async def get_track_by_url(self, url: str) -> Track:
        track = await self._ym_client.get_track_by_url(url=url)
        return await self._ym_track_to_track(track=track, source=url)

    async def get_playlist_by_url(self, url: str) -> Playlist:
        playlist, tracks = await self._ym_client.get_playlist_with_tracks_by_url(url=url)
        return await self._ym_playlist_to_playlist(playlist=playlist, tracks=tracks, source=url)

    async def get_album_by_url(self, url: str) -> Playlist:
        album, tracks = await self._ym_client.get_album_with_tracks_by_url(url=url)
        return await self._ym_album_to_playlist(album=album, tracks=tracks, source=url)

    async def get_audio_sources_by_url(self, url: str) -> tuple[AudioSource, ...]:
        return self._wrap_with_audio_source(await self._ym_client.get_audio_sources_by_url(url=url))

    async def get_lyrics_by_url(self, url: str) -> str:
        return await self._ym_client.get_lyrics_by_url(url=url)

    async def get_audio_sources_for_track(self, track: Track) -> tuple[AudioSource, ...]:
        if track.raw is not None and isinstance(track.raw, yandex_music.Track):
            return self._wrap_with_audio_source(await self._ym_client.get_audio_sources_by_raw(raw=track.raw))

        return await self.get_audio_sources_by_url(url=track.source)

    async def get_lyrics_for_track(self, track: Track) -> str:
        if track.raw is not None and isinstance(track.raw, yandex_music.Track):
            return await self._ym_client.get_lyrics_by_raw(raw=track.raw)
        return await self._ym_client.get_lyrics_by_url(url=track.source)

    async def search_track_by_name(self, query: str) -> Optional[Track]:
        tracks = await self._ym_client.search_track_by_name(query)

        if not tracks:
            return None

        best_match_track = tracks[0]
        best_match_track.variations = tracks[1:]

        return best_match_track

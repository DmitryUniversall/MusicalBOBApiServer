import re
from typing import Container, Final
from urllib.parse import unquote

_SCHEME_REGEX: Final[re.Pattern] = re.compile(r"\A\s*[a-z][a-z0-9+.\-]*://", re.IGNORECASE)
_INVISIBLE_REGEX: Final[re.Pattern] = re.compile(r"[​-‏‪-‮⁦-⁩﻿]")


def has_url_scheme(text: str) -> bool:
    """
    Checks whether `text` starts with a url scheme (`https://`, `yandexmusic://`, ...).

    :param text: `str`
        Raw text.

    :return: `bool`
        `True` if a scheme is present.
    """

    return _SCHEME_REGEX.match(text) is not None


def normalize_url(raw: str) -> str:
    """
    Prepares user-provided text to be parsed as a url.

    Strips surrounding whitespace, markup-ish wrapping characters and invisible codepoints
    (messengers and note-taking apps insert those), and assumes `https` for scheme-less input.

    :param raw: `str`
        Raw user input.

    :return: `str`
        Url with a scheme, safe to pass to `urlsplit`.
    """

    text = _INVISIBLE_REGEX.sub("", raw).strip().strip("<>\"'")

    return text if has_url_scheme(text) else f"https://{text}"


def url_segments(path: str) -> list[str]:
    """
    Splits a url path into decoded, non-empty segments.

    :param path: `str`
        Url path.

    :return: `list[str]`
        Decoded segments, without empty ones produced by leading/trailing/doubled slashes.
    """

    return [unquote(segment) for segment in path.split("/") if segment]


def keyword_pairs(segments: list[str], keywords: Container[str]) -> dict[str, str]:
    """
    Collects `<keyword>/<value>` pairs anywhere in the path.

    Position-independent on purpose: for path-based resource ids, an added prefix
    (`/ru/album/1`) or a trailing sub-page (`/artist/1/tracks`) must not break parsing.

    :param segments: `list[str]`
        Decoded path segments.

    :param keywords: `Container[str]`
        Lowercase keywords that are expected to be followed by a value.

    :return: `dict[str, str]`
        Mapping of keyword to the segment following it (first occurrence wins).
    """

    pairs: dict[str, str] = {}

    index = 0
    while index < len(segments) - 1:
        keyword = segments[index].lower()

        if keyword in keywords and keyword not in pairs:
            pairs[keyword] = segments[index + 1]
            index += 2
        else:
            index += 1

    return pairs

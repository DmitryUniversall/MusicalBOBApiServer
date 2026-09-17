import re
from typing import Final

UUID_REGEX: Final[str] = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

HTTP_SCHEMES: Final[frozenset[str]] = frozenset({"http", "https"})

URL_SCHEME_REGEX: Final[re.Pattern] = re.compile(r"\A\s*[a-z][a-z0-9+.\-]*://", re.IGNORECASE)

# Zero-width and bidirectional control characters, inserted by messengers and note-taking apps
INVISIBLE_CHARS_REGEX: Final[re.Pattern] = re.compile(r"[​-‏‪-‮⁦-⁩﻿]")

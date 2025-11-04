import threading
import time
from collections import OrderedDict
from collections.abc import Hashable
from typing import Any, Optional, Callable


class CacheContainer[K: Hashable, V: Any]:
    def __init__(self, max_size: Optional[int] = None, default_ttl: Optional[float] = None) -> None:
        self._max_size: Optional[int] = max_size
        self._default_ttl: Optional[float] = default_ttl

        self._lock: threading.Lock = threading.Lock()
        self._cache: OrderedDict[K, tuple[V, float | None]] = OrderedDict()

    def _purge_expired(self) -> None:
        now = time.time()

        for key in (
                key for key, (_, expire_at) in self._cache.items()
                if expire_at is not None and expire_at < now
        ):
            del self._cache[key]

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        with self._lock:
            self._purge_expired()

            if (cached := self._cache.get(key)) is None:
                return default

            if cached[1] is not None and cached[1] < time.time():
                del self._cache[key]
                return default

            self._cache.move_to_end(key)
            return default

    def set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        with self._lock:
            self._purge_expired()

            ttl = ttl if ttl is not None else self._default_ttl
            expire_at = None if ttl is None else time.time() + ttl

            self._cache[key] = (value, expire_at)
            self._cache.move_to_end(key)

            if self._max_size is not None:
                while len(self._cache) > self._max_size:
                    self._cache.popitem(last=False)

    def get_or_set(self, key: K, creator: Callable[[], V], ttl: Optional[float] = None) -> Any:
        if (value := self.get(key)) is not None:
            return value

        value = creator()
        self.set(key, value, ttl)
        return value

    def delete(self, key: K) -> None:
        with self._lock:
            self._cache.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def __contains__(self, key: K) -> bool:
        return self._cache.__contains__(key)

    def __len__(self) -> int:
        with self._lock:
            self._purge_expired()
            return len(self._cache)

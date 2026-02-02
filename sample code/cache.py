import threading
from typing import Any, Optional


class CacheError(Exception):
    """Raised when a cache operation fails."""


class Cache:
    def __init__(self):
        self.store = {}
        self._lock = threading.RLock()

    def get(self, key: Any) -> Optional[Any]:
        try:
            with self._lock:
                return self.store.get(key)
        except Exception as e:
            raise CacheError(f"Error getting key {key}: {e}") from e

    def set(self, key: Any, value: Any) -> None:
        try:
            with self._lock:
                self.store[key] = value
        except Exception as e:
            raise CacheError(f"Error setting key {key}: {e}") from e

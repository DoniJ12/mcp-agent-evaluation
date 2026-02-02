from cache import Cache, CacheError
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)
cache = Cache()


def get_user(user_id: Any) -> Optional[dict]:
    """Return user dict for a given integer user_id.

    Validates input, falls back to DB on cache errors, and retries cache writes.
    """
    if not isinstance(user_id, int):
        raise TypeError("user_id must be an integer")
    if user_id <= 0:
        raise ValueError("user_id must be positive")

    try:
        user = cache.get(user_id)
    except CacheError as e:
        logger.warning("Cache get failed for %s: %s", user_id, e)
        user = None

    if user is not None:
        return user

    # simulate database fetch
    try:
        if user_id == 1:
            user = {"id": 1, "name": "Alice"}
        else:
            user = None
    except Exception:
        logger.exception("Database fetch failed for %s", user_id)
        raise

    # attempt to cache result with retries
    for attempt in range(3):
        try:
            cache.set(user_id, user)
            break
        except CacheError as e:
            logger.warning("Cache set failed for %s (attempt %d): %s", user_id, attempt + 1, e)
            if attempt == 2:
                logger.error("Giving up setting cache for %s", user_id)

    return user

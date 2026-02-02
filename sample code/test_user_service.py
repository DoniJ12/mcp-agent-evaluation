import unittest

from cache import CacheError


class DummyCache:
    def __init__(self, get_behavior=None, set_behavior=None):
        self._data = {}
        self.get_behavior = get_behavior
        self.set_behavior = set_behavior
        self.set_calls = 0

    def get(self, key):
        if isinstance(self.get_behavior, Exception):
            raise self.get_behavior
        if callable(self.get_behavior):
            return self.get_behavior(key)
        return self._data.get(key)

    def set(self, key, value):
        self.set_calls += 1
        if isinstance(self.set_behavior, Exception):
            raise self.set_behavior
        if callable(self.set_behavior):
            return self.set_behavior(key, value)
        self._data[key] = value


class UserServiceTests(unittest.TestCase):
    def setUp(self):
        import user_service

        self.user_service = user_service
        self._real_cache = user_service.cache

    def tearDown(self):
        # restore original cache
        self.user_service.cache = self._real_cache

    def test_get_user_cached(self):
        dummy = DummyCache()
        dummy._data[1] = {"id": 1, "name": "Cached"}
        self.user_service.cache = dummy

        user = self.user_service.get_user(1)
        self.assertEqual(user, {"id": 1, "name": "Cached"})

    def test_get_user_db_and_cache_set(self):
        dummy = DummyCache()
        self.user_service.cache = dummy

        user = self.user_service.get_user(1)
        self.assertEqual(user, {"id": 1, "name": "Alice"})
        self.assertIn(1, dummy._data)

    def test_get_user_missing_returns_none(self):
        dummy = DummyCache()
        self.user_service.cache = dummy

        user = self.user_service.get_user(2)
        self.assertIsNone(user)

    def test_cache_get_raises_but_db_still_returns(self):
        dummy = DummyCache(get_behavior=CacheError("get fail"))
        self.user_service.cache = dummy

        user = self.user_service.get_user(1)
        self.assertEqual(user, {"id": 1, "name": "Alice"})

    def test_validation_errors(self):
        with self.assertRaises(TypeError):
            self.user_service.get_user("bad")
        with self.assertRaises(ValueError):
            self.user_service.get_user(0)


if __name__ == "__main__":
    unittest.main()

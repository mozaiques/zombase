# -*- coding: utf-8 -*-


class ComputedValuesData():
    """Unified interface for cache systems."""

    def __init__(self):
        self.cache_systems = []

    def append_cache(self, cache):
        """Append a cache system to the interface."""
        self.cache_systems.append(cache)

    def get(self, key):
        """Return the first value found by browsing the cache systems."""
        for cache in self.cache_systems:
            val = cache.get(key)
            if val is not None:
                return val
        return None

    def set(self, key, value):
        """Set the value in all the cache systems."""
        for cache in self.cache_systems:
            cache.set(key, value)

    def expire(self, key):
        """Expire the value in all the cache systems."""
        for cache in self.cache_systems:
            cache.expire(key)

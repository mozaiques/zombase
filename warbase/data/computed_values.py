class ComputedValuesData():

    def __init__(self, **kwargs):
        self.cache_systems = []

    def append_cache(self, cache):
        self.cache_systems.append(cache)

    def get(self, **kwargs):

        for cache in self.cache_systems:
            val = cache.get(**kwargs)
            if val is not None:
                return val

        return None

    def set(self, **kwargs):

        for cache in self.cache_systems:
            cache.set(**kwargs)

    def expire(self, **kwargs):

        for cache in self.cache_systems:
            cache.expire(**kwargs)

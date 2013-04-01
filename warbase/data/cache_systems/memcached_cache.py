import pylibmc


class MemcachedCache():

    def __init__(self, **kwargs):
        if not 'server' in kwargs:
            raise TypeError('server not provided')

        self._server = kwargs['server']
        self._cache = pylibmc.Client([self._server])

    def _check_key(self, **kwargs):
        if 'key' not in kwargs:
            raise TypeError('Key informations not provided')

        if not isinstance(kwargs['key'], str):
            raise AttributeError('key provided is not a string')

    def _split_key(self, key):
        split_key = key.split(':')
        if len(split_key) != 3:
            return False

        return ['{}:{}'.format(split_key[0], split_key[1])] + split_key[2:]

    def get(self, force=False, **kwargs):
        self._check_key(**kwargs)

        split_key = self._split_key(kwargs['key'])
        if not split_key or not split_key[1]:
            return False

        cache_key = self._cache.get(split_key[0])

        if not cache_key or not split_key[1] in cache_key:
            return False

        return cache_key[split_key[1]]

    def set(self, **kwargs):
        self._check_key(**kwargs)

        if 'value' not in kwargs:
            raise TypeError('Value informations not provided')

        split_key = self._split_key(kwargs['key'])
        if not split_key or not split_key[1]:
            raise AttributeError('Incorrect key')

        cache_key = self._cache.get(split_key[0])
        if not cache_key:
            cache_key = {}

        cache_key[split_key[1]] = kwargs['value']

        self._cache.set(split_key[0], cache_key)

    def expire(self, **kwargs):
        self._check_key(**kwargs)

        split_key = self._split_key(kwargs['key'])

        if not split_key[1]:
            self._cache.delete(split_key[0])
            return

        cache_key = self._cache.get(split_key[0])
        cache_key.pop(split_key[1], None)
        self._cache.set(split_key[0], cache_key)

# -*- coding: utf-8 -*-
from sqlalchemy.orm import object_session
from dogpile.cache.api import NoValue


def cached_property(key_template, ksk_tpl=None, cache=None):
    """Decorator for a method of a SQLA-object.

    Act like the `@property` decorator, but handle interactions with
    the cache.

    Value will be stored with the key provided in `key_template`, and
    key will be added to the stores whose key are provided in `ksk_tpl`.

    Argument:
        key_template -- template of the key that will be used in cache.

    Keyword argument:
        ksk_tpl -- string or list
                   default: object._key_store_key_template

                   Key's template(s) of the store(s) in which a
                   potential new key will be added. Useful to track
                   dependencies. (means key_store_key_templates)

        cache -- dogpile.cache region
                 default: object_session(object).cache

                 dogpile.cache's region which will be used.

    Example usage:

        @cached_property('prestation:{prestation.id}:margin')
        def margin(self):
            return self.selling_price - self.cost

    """

    def decorator(func):

        def wrapped(self, *args, **kwargs):
            if cache:
                _cache = getattr(self, cache)
            else:
                _cache = object_session(self).cache

            format_dict = dict(instance=self)

            key = key_template.format(**format_dict)
            cache_value = _cache.get(key)

            # If we have the value in cache, we just return it.
            if not isinstance(cache_value, NoValue):
                return cache_value

            # Run the computation
            value = func(self, *args, **kwargs)

            # Store value in cache
            _cache.set(key, value)

            if ksk_tpl is None:
               ksk = self._key_store_key_template.format(**format_dict)
               key_stores = [ (ksk, _cache.get(ksk)) ]

            elif isinstance(ksk_tpl, basestring):
                ksk = ksk_tpl.format(**format_dict)
                key_stores = [ (ksk, _cache.get(ksk)) ]

            elif isinstance(ksk_tpl, list):
                key_stores = list()
                for key_tpl in ksk_tpl:
                    ksk = key_tpl.format(**format_dict)
                    key_stores.append((ksk, _cache.get(ksk)))

            else:
                raise AttributeError('ksk_tpl must be a string or a list')

            for (key_store_key, key_store) in key_stores:
                # If the key_store hasn't been created yet, we initialize it
                if isinstance(key_store, NoValue):
                    key_store = []

                key_store.append(key)
                _cache.set(key_store_key, key_store)

            return value

        return property(wrapped)

    return decorator

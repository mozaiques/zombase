# -*- coding: utf-8 -*-
import os
import imp


class ConfigError(KeyError):
    pass


class Config(dict):
    """Works exactly like a dict but provides ways to fill it from files
    or special dictionaries.

    Extracted from Flask source, see:
        - file: flask/config.py
        - commit: 52098e1e4fc4d9c962e9ecb09dfbbcc6ac80a4d7

    """

    def __getitem__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            raise ConfigError(
                'The requested config value, {}, is not set'.format(name))

    def from_envvar(self, variable_name):
        rv = os.environ.get(variable_name)
        if rv:
            return self.from_pyfile(rv)
        raise RuntimeError(
            'The environment variable {} is not set.'.format(variable_name))

    def from_pyfile(self, filename):
        d = imp.new_module('config')
        d.__file__ = filename
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), d.__dict__)

        self.from_object(d)
        return True

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def from_dict(self, a_dict):
        for key in a_dict:
            if key.isupper():
                self[key] = a_dict[key]

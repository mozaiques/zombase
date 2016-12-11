zombase Changelog
=================

Version 0.8.1
------------

- Add `ignore_keys` to `zombase.mapping.update`

Version 0.8.0
------------

- Remove cache support
- Add guard to Decimable/Floatable to avoid NaN

Version 0.4.0
------------

- Change relation between `worker._get()`, `worker.get()` and mapping
  id's (`id` and `uuid`)). Might break bc.
- Fix `worker._resolve_id()` for Python3.
- Fix `config` for Python3.

Version 0.1.0
------------

- We start here

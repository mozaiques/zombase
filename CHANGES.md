mozbase Changelog
================

Version 0.4.5
------------

- BREAKING: Fix `ObjectManagingDataRepository._update()` behavior to set
  values returned by the schema, thus allowing schema to mutate values.
- `ObjectManagingDataRepository._resolve_id()` now has `allow_none_id`
  option to unset relation (setting it to 'None').
- Add `util.validation.SchemaDictNone` to ease schema description.
- Add `util.validation.Floatable` which improves `voluptuous.Coerce`.

# Changelog

All notable changes to this project will be documented in this file.

## [0.0.25] - 2025-01-15

### Added

- Added `has_namespace` and `id` properties to `AnonymousNamespace` class to handle non-activated/anonymous orgs.
- Ensure view tests run first with [tests/conftest.py](tests/conftest.py).

## [0.0.24] - 2025-01-15

### Added

- Renamed default setting names to start with `DJANGO_NAMESPACES_` to avoid conflicts with other apps.

## [0.0.23] - 2025-01-15

### Added

- If using a swappable Namespace model, unregister the default Namespace model from admin.

## [0.0.22] - 2025-01-14

### Added

- Minor bug fixes

## [0.0.21] - 2025-01-14

### Added

- swappable model for Namespace. Defaults to `DJANGO_NAMESPACES_NAMESPACE_MODEL="django_namespaces.Namespace"`.
- Abstract model for Namespace.
- Checks for Namespace model.
- New test cases

## [0.0.20] - 2025-01-13

- An updated changelog is coming soon.

## [0.0.01] - [0.0.19] - 2025-01-13

- Old versions removed.

[0.0.24]: https://github.com/jmitchel3/django-namespaces/compare/v0.0.24...HEAD
[0.0.23]: https://github.com/jmitchel3/django-namespaces/compare/v0.0.23...v0.0.24
[0.0.22]: https://github.com/jmitchel3/django-namespaces/compare/v0.0.22...v0.0.23
[0.0.21]: https://github.com/jmitchel3/django-namespaces/compare/v0.0.21...v0.0.22
[0.0.20]: https://github.com/jmitchel3/django-namespaces/compare/v0.0.20...v0.0.21

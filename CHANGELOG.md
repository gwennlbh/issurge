# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-05-02

### Added

- On github repositories in organizations, using `~issuetype` will now set the issue's type instead of adding a label, if `issuetype` case-insensitively matches one of the issue's organization's issue types. Setting multiple issue types results in an error.

## [1.0.1] - 2025-05-02

### Fixed

- Fixed an issue where a issue reference was not replaced when followed by a non-space punctuation character (e.g. `see #.1, #.2` would not replace `#.1`) (#15)

## [1.0.0] - 2025-05-01

### Added

- `--open` to open created issue(s) in the browser

## [0.6.4] - 2025-04-30

### Changed

- Nothing, just a CI fail on the previous release 🥺

## [0.6.3] - 2025-04-30

### Changed

- Upgraded dependencies

## [0.6.2] - 2025-04-30

### Changed

- Support Python ≥ 3.12 again (by migrating away from [ward](https://github.com/darrenburns/ward) to pytest)

## [0.6.1] - 2025-02-19

### Fixed

- Previous release seemingly contained no changes?
- Prevent strict reference resolving in dry-run mode

## [0.6.0] - 2025-02-19

### Added

- Add support for referecing not-yet-created issues! see [#13](https://github.com/gwennlbh/issurge/issues/13)

## [0.5.0] - 2024-07-13

### Added

- support for ssh remotes

## [0.4.1] - 2024-01-02

### Added

- a setup.py script for AUR deployment

## [0.4.0] - 2023-04-02

### Added

- one-shot mode (see #1)

## [0.3.0] - 2023-04-02

### Changed

- words that start with a sigil (labels, milestones, assignees) and are in the middle of a title are now added to the title, without the sigil (see README.md for more explanations)

### Fixed

- crashes

## [0.2.0] - 2023-04-02

### Added

- Github support (requires gh to be installed)
- Initial release.

## [0.1.0]

[Unreleased]: https://github.com/gwennlbh/issurge/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/gwennlbh/issurge/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/gwennlbh/issurge/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/gwennlbh/issurge/compare/v0.6.2...v1.0.0
[0.6.3]: https://github.com/gwennlbh/issurge/compare/v0.6.2...v0.6.3
[0.6.2]: https://github.com/gwennlbh/issurge/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/gwennlbh/issurge/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/gwennlbh/issurge/compare/v0.5.0...v0.5.0
[0.5.0]: https://github.com/gwennlbh/issurge/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/gwennlbh/issurge/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/gwennlbh/issurge/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/gwennlbh/issurge/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/gwennlbh/issurge/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/gwennlbh/issurge/releases/tag/v0.1.0

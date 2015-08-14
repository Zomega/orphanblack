# Change Log

All notable changes to this project will be documented in this file.
With the exeception of the 0.\*.\* versions, this project adheres to [Semantic Versioning](http://semver.org/).

The 0.\*.\* versions represent an early alpha / complete rewrite of an old tool, so there are a lot of breaking changes between every version, even if the broad strokes stay the same.

The format of this changelog was informed by the guidlines at [keepachangelog.com](http://keepachangelog.com/)

## [Planned / Wishlist][planned]

* Multilanguage support
* Plugin API
* Algorithm rewrite

## [Unreleased][unreleased]

Nothing yet!

## [0.2.0] - 2015-08-13
### Added
* Detailed documentation, including this Change Log.
* Manifests for fine grained selection of input files. Each language now also has a default manifest that will be used if nothing is specified.

### Removed
* All settings related to configuring the exact parameters of the underlying algorithm. These will be replaced with a detailed configuration system slated for the next release.

* Many settings related to specifying files from the CLI. All files my now be either explicitly passed in by name, or defined via a manifest.

### Changed
* Replaced ad-hoc error reporting system with `logging`, all previous messages are printed on `INFO` UNLESS they were explicitly specified as a warning (in which case they are `WARNING`), or were fatal (called `sys.exit(1)`, which are now rated `ERROR`).

### Fixed
* A few bugs related to code that would only run when the program was run in verbose mode; it is now safe / possible to use lower verbosity by specifying a `logging` level.

### Security
* Reports are no longer stored on disk using pickle; they are serialized in JSON instead.

## [0.1.11] - 2015-08-09
This initial release repackaged clonedigger and made several coarse improvements.

### Added

* Initial code base (mostly due to clonedigger)
* Basic command line functions (uses Click)
* Report persistence based on pickle
* Clarified README.md and LICENSE.txt from clonedigger copies
* Jinja2-based html templates

[planned]: https://github.com/Zomega/orphanblack/milestones
[unreleased]: https://github.com/Zomega/orphanblack/compare/v0.2.0...develop
[0.2.0]: https://github.com/Zomega/orphanblack/compare/v0.1.11...v0.2.0
[0.1.11]: https://github.com/Zomega/orphanblack/tree/v0.1.11
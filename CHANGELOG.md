# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive README.md with installation, usage examples, and project overview
- Detailed TODO.md with structured development roadmap
- CONTRIBUTING.md with contribution guidelines
- CHANGELOG.md for tracking project changes

### Changed
- Updated documentation to reflect current codebase structure
- Reorganized roadmap to show realistic milestones

## [0.1.0] - 2025

### Added
- Complete codebase reorganization with modern Python structure
- Core music theory modules (notes, scales, chords, intervals, drums, patterns)
- Algorithmic composition tools (evolutionary cantus firmus, voice leading)
- MIDI processing capabilities (extraction, analysis, drum patterns)
- Audio processing tools (sampling, harmonic analysis)
- Machine learning infrastructure (GPT-2 based models, training pipeline)
- Command-line interfaces (generate, train, analyze)
- Modern pyproject.toml with optional dependencies
- Support for Python 3.8-3.12
- Modular architecture with optional ML components

### Changed
- Migrated from root-level scripts to organized `scripts/` directory
- Separated music theory (core) from generation algorithms
- Improved error handling throughout the codebase
- Added type hints to ML modules
- Modernized package structure following best practices

### Deprecated
- Root-level scripts (generate_sequence.py, trainer.py, drum_extract.py)
- Old import paths (now redirected to new structure)

### Removed
- Chaotic mixture of scripts in root directory
- Hardcoded paths in old scripts
- Poor error handling in legacy code

## [Pre-0.1.0]

Previous development history before major reorganization.

---

[Unreleased]: https://github.com/matias-ceau/harmonics/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/matias-ceau/harmonics/releases/tag/v0.1.0

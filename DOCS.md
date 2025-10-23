# Documentation Index

Welcome to Harmonics documentation! This guide helps you navigate all available documentation.

## Getting Started

- **[README.md](README.md)** - Project overview, installation, quick start, and features
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project
- **[TODO.md](TODO.md)** - Development roadmap and planned features

## Project History & Migration

- **[MODERNIZATION_SUMMARY.md](MODERNIZATION_SUMMARY.md)** - Overview of recent codebase reorganization
- **[DEPRECATED_SCRIPTS.md](DEPRECATED_SCRIPTS.md)** - Migration guide from old scripts to new structure
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

## Core Documentation

### Installation

See [README.md](README.md#installation) for:
- Basic installation
- ML support installation
- Development installation

### Usage Examples

See [README.md](README.md#quick-start) for:
- Music theory basics
- Algorithmic composition
- Audio/MIDI processing
- Machine learning generation

### Command Line Tools

See [README.md](README.md#command-line-interface) and [scripts/README.md](scripts/README.md) for:
- `harmonics-generate` - Music generation
- `harmonics-train` - Model training
- `harmonics-analyze` - File analysis

## Architecture

### Module Structure

From [README.md](README.md#project-structure):

```
src/harmonics/
├── core/         - Music theory fundamentals (notes, scales, chords)
├── generation/   - Algorithmic composition (cantus, voice leading)
├── processing/   - Audio/MIDI I/O and analysis
├── ml/           - Machine learning models (optional)
├── cli/          - Command-line interfaces
└── symbols/      - Abstract musical symbols
```

### Design Principles

From [MODERNIZATION_SUMMARY.md](MODERNIZATION_SUMMARY.md):
- Modular architecture with clear separation
- Optional ML dependencies
- Professional CLI interfaces
- Backward compatibility during transition

## Development

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development workflow
- Code style guidelines
- Testing requirements
- Pull request process

### Roadmap

See [TODO.md](TODO.md) for:
- Current priorities (v0.1.x)
- Near-term plans (v0.2.x)
- Mid-term goals (v0.3.x)
- Long-term vision (v1.0+)

### Code Quality

Development tools configured in [pyproject.toml](pyproject.toml):
- **Black**: Code formatting
- **Ruff**: Fast linting
- **MyPy**: Type checking
- **Pytest**: Testing framework

## API Reference

### Core Modules

- **harmonics.core**: Music theory (notes, scales, chords, intervals)
- **harmonics.generation**: Algorithmic composition
- **harmonics.processing**: Audio and MIDI processing
- **harmonics.ml**: Machine learning (requires optional dependencies)
- **harmonics.cli**: Command-line interfaces
- **harmonics.symbols**: Abstract musical objects

### Legacy Modules

For backward compatibility, these are still available but use new structure internally:
- harmonics.audio → harmonics.processing.audio
- harmonics.midi → harmonics.processing.midi
- harmonics.data → harmonics.core
- harmonics.theory → harmonics.generation

See [DEPRECATED_SCRIPTS.md](DEPRECATED_SCRIPTS.md) for migration details.

## Additional Resources

### Scripts

- [scripts/README.md](scripts/README.md) - Standalone script documentation
- [scripts/generate_music.py](scripts/generate_music.py) - Music generation
- [scripts/train_model.py](scripts/train_model.py) - Model training
- [scripts/extract_midi.py](scripts/extract_midi.py) - MIDI extraction

### Configuration

- [pyproject.toml](pyproject.toml) - Package configuration and metadata
- [tox.ini](tox.ini) - Testing configuration
- [.gitignore](.gitignore) - Version control exclusions

### Data

- [data/](data/) - Example audio and MIDI files
- Sample files for testing and demonstration

## Support

- **Issues**: https://github.com/matias-ceau/harmonics/issues
- **Repository**: https://github.com/matias-ceau/harmonics

## License

GPL-3.0-or-later - See [LICENSE](LICENSE)

---

**Quick Links:**
- [Installation](README.md#installation) | [Quick Start](README.md#quick-start) | [Contributing](CONTRIBUTING.md) | [Roadmap](TODO.md) | [Changelog](CHANGELOG.md)

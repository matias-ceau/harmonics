# Harmonics 🎵

A comprehensive Python library for music theory, analysis, algorithmic composition, and machine learning-based music generation.

## Overview

Harmonics provides a modular toolkit for working with music at multiple levels:

- **Music Theory**: Core abstractions for notes, scales, chords, intervals, and harmony
- **Algorithmic Composition**: Rule-based generation including counterpoint and evolutionary algorithms
- **Audio/MIDI Processing**: Tools for analyzing and manipulating audio and MIDI data
- **Machine Learning**: Neural network models for music sequence generation
- **Command Line Tools**: Professional CLI interfaces for common workflows

## Installation

### Basic Installation

For core music theory and algorithmic composition features:

```bash
pip install -e .
```

### With Machine Learning Support

To use neural network-based music generation:

```bash
pip install -e ".[ml]"
```

### Development Installation

For contributors:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Music Theory

```python
from harmonics.core import notes, scales, chords

# Work with musical notes
note = notes.Note("C4")
scale = scales.Scale("C", "major")
chord = chords.Chord("Cmaj7")
```

### Algorithmic Composition

```python
from harmonics.generation import cantus

# Generate a cantus firmus using evolutionary algorithm
population, generations = cantus.run_evolution(
    sequence_length=12,
    key_center=0,
    population_size=100,
    generation_limit=50
)
```

### Audio Analysis

```python
from harmonics.processing.audio import get_harmonics

# Extract harmonic content from audio
harmonics_data = get_harmonics("audio_file.wav")
```

### MIDI Processing

```python
from harmonics.processing.midi import extract_midi_data

# Extract and analyze MIDI data
midi_data = extract_midi_data("song.mid")
```

### Machine Learning Generation

```python
from harmonics.ml import MusicGenerator

# Generate music using trained models
generator = MusicGenerator("path/to/model")
sequence = generator.generate(prompt="^", temperature=0.7)
```

## Command Line Interface

Harmonics provides three main CLI commands:

### Generate Music

```bash
# Using ML models
harmonics-generate ml --model-path ./trained_model --prompt "^" --temperature 0.7

# Using evolutionary algorithms
harmonics-generate cantus --length 12 --key 0 --generations 50
```

### Train Models

```bash
harmonics-train --tokens data.pt --epochs 50 --output-dir ./models --batch-size 32
```

### Analyze Files

```bash
# Batch analyze MIDI files
harmonics-analyze batch midi_files.txt --output-dir ./analysis

# Single file analysis
harmonics-analyze file song.mid --output-dir ./analysis
```

## Project Structure

```
harmonics/
├── src/harmonics/
│   ├── core/              # Music theory fundamentals
│   │   ├── notes.py       # Note representation
│   │   ├── scales.py      # Scales and modes
│   │   ├── chords.py      # Chord structures
│   │   └── intervals.py   # Musical intervals
│   ├── generation/        # Algorithmic composition
│   │   ├── cantus.py      # Cantus firmus generation
│   │   ├── voice.py       # Voice leading
│   │   └── functions.py   # Generation utilities
│   ├── processing/        # Audio/MIDI processing
│   │   ├── audio/         # Audio analysis
│   │   └── midi/          # MIDI extraction
│   ├── ml/                # Machine learning
│   │   ├── models.py      # Neural network models
│   │   ├── training.py    # Training utilities
│   │   └── generation.py  # ML generation
│   ├── cli/               # Command line interfaces
│   │   ├── generate.py    # Generation commands
│   │   ├── train.py       # Training commands
│   │   └── analyze.py     # Analysis commands
│   └── symbols/           # Abstract musical symbols
│       ├── note.py        # Note symbols
│       ├── chord.py       # Chord symbols
│       └── pattern.py     # Pattern symbols
├── scripts/               # Standalone scripts
│   ├── generate_music.py  # Generate sequences
│   ├── train_model.py     # Train ML models
│   └── extract_midi.py    # Extract MIDI data
├── data/                  # Example data and test files
└── tests/                 # Test suite (TODO)
```

## Features

### ✅ Implemented

- **Core Music Theory**: Notes, scales, chords, intervals, drums, patterns
- **Algorithmic Generation**: Evolutionary cantus firmus generation, voice leading
- **MIDI Processing**: MIDI extraction, drum pattern extraction, analysis tools
- **Audio Processing**: Harmonic analysis, audio feature extraction
- **ML Infrastructure**: GPT-2 based models, training pipeline, generation tools
- **CLI Tools**: Complete command-line interfaces for all major features
- **Modern Package Structure**: Clean modular architecture with optional ML dependencies

### 🚧 In Progress

- Test suite implementation
- Documentation improvements
- Example notebooks
- Pre-trained model distribution

### 📋 Planned

See [TODO.md](TODO.md) for detailed roadmap.

## Development

### Code Style

This project uses modern Python tooling:

- **Black**: Code formatting
- **Ruff**: Fast linting
- **MyPy**: Type checking
- **Pytest**: Testing framework

Run linters:

```bash
black src/
ruff check src/
mypy src/
```

### Architecture

The codebase follows a modular architecture with clear separation of concerns:

- `core/`: Pure music theory (no ML dependencies)
- `generation/`: Algorithmic composition (no ML dependencies)
- `processing/`: Audio/MIDI I/O and analysis
- `ml/`: Machine learning components (optional dependencies)
- `cli/`: Command line interfaces

This structure allows users to install only what they need and ensures core functionality is always available.

## Migration from Old Structure

If you're updating from an older version of harmonics, see [DEPRECATED_SCRIPTS.md](DEPRECATED_SCRIPTS.md) and [MODERNIZATION_SUMMARY.md](MODERNIZATION_SUMMARY.md) for migration guidance.

## License

GPL-3.0-or-later - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run linters and tests
5. Submit a pull request

## Resources

- **Repository**: https://github.com/matias-ceau/harmonics
- **Issues**: https://github.com/matias-ceau/harmonics/issues

## Citation

If you use Harmonics in academic work, please cite:

```bibtex
@software{harmonics,
  author = {Matias Ceau},
  title = {Harmonics: Music Analysis and Creation Library},
  year = {2025},
  url = {https://github.com/matias-ceau/harmonics}
}
```

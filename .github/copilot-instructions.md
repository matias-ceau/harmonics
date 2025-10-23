# Copilot Instructions for Harmonics

## Project Overview

Harmonics is a Python library for music analysis and creation. It provides tools for working with MIDI, audio processing, music theory, machine learning models for music generation, and various analysis features.

## Project Structure

- `src/harmonics/`: Main package source code
  - `audio/`: Audio processing utilities
  - `bass/`, `melody/`, `groove/`: Music component analysis
  - `midi/`: MIDI file handling
  - `ml/`: Machine learning models for music generation
  - `theory/`: Music theory utilities
  - `processing/`: Signal processing
  - `cli/`: Command-line interfaces
  - `core/`: Core functionality
- `tests/`: Test suite (pytest)
- `data/`: Data files
- `scripts/`: Utility scripts

## Development Standards

### Python Version
- Target Python >= 3.8
- Support Python 3.8, 3.9, 3.10, 3.11, 3.12

### Code Style
- **Formatter**: Use `black` with 88 character line length
- **Linter**: Use `ruff` for code quality checks
- **Type Checking**: Use `mypy` with strict type checking enabled
- Follow PEP 8 conventions
- Use type hints for all function signatures

### Code Quality Tools Configuration
All tools are configured in `pyproject.toml`:
- Black: 88 char line length, targets py38-py312
- Ruff: Enforces pycodestyle, pyflakes, isort, flake8-bugbear, comprehensions, and pyupgrade
- MyPy: Strict type checking with disallow_untyped_defs enabled

### Testing
- Use `pytest` for testing
- Place tests in the `tests/` directory
- Test files should be named `test_*.py`
- Aim for good test coverage
- Run tests with coverage reporting: `pytest --cov=harmonics --cov-report=term-missing`

## Dependencies

### Core Dependencies
- numpy, scipy: Numerical computing
- pandas: Data manipulation
- matplotlib, seaborn: Visualization
- mido, python-rtmidi: MIDI handling
- pyyaml: Configuration files

### Optional Dependencies
- `ml` extras: PyTorch, transformers, tensorboard for machine learning features
- `dev` extras: Development tools (black, ruff, mypy, pytest, pytest-cov)

## CLI Applications
The package provides three command-line tools:
- `harmonics-generate`: Music generation
- `harmonics-train`: Model training
- `harmonics-analyze`: Music analysis

## Build System
- Uses setuptools with pyproject.toml configuration
- Package structure follows src-layout pattern
- Build with: `pip install -e .` or `pip install -e .[dev,ml]`

## Coding Guidelines

1. **Type Hints**: Always use type hints for function parameters and return values
2. **Docstrings**: Use clear docstrings for all public functions and classes
3. **Error Handling**: Use appropriate exception handling and custom exceptions where needed
4. **Imports**: Keep imports organized (use ruff/isort for automatic sorting)
5. **Music Domain**: Be aware of music theory concepts, MIDI standards, and audio processing conventions
6. **Performance**: Consider numpy/scipy vectorization for performance-critical code
7. **Compatibility**: Ensure code works across Python 3.8-3.12

## When Making Changes

1. Run code formatter: `black src/`
2. Run linter: `ruff check src/`
3. Run type checker: `mypy src/`
4. Run tests: `pytest`
5. Check coverage: `pytest --cov=harmonics`

## License
GNU General Public License v3.0 or later (GPLv3+)

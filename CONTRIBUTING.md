# Contributing to Harmonics

Thank you for your interest in contributing to Harmonics! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/harmonics.git
   cd harmonics
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install in development mode**:
   ```bash
   pip install -e ".[dev,ml]"
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Add tests** for new functionality

4. **Run the test suite**:
   ```bash
   pytest
   ```

5. **Check code style**:
   ```bash
   black src/
   ruff check src/
   mypy src/
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Submit a pull request** on GitHub

## Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use **Black** for code formatting (line length: 88)
- Use **type hints** for all function signatures
- Write **docstrings** for all public functions/classes (Google style)

Example:
```python
def generate_sequence(
    prompt: str,
    temperature: float = 0.7,
    max_length: int = 100
) -> str:
    """Generate a music sequence from a prompt.
    
    Args:
        prompt: Starting sequence for generation
        temperature: Sampling temperature (higher = more random)
        max_length: Maximum length of generated sequence
        
    Returns:
        Generated music sequence as a string
        
    Raises:
        ValueError: If temperature is not positive
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    # Implementation...
```

### Import Organization

Order imports as:
1. Standard library
2. Third-party packages
3. Local imports

Use absolute imports for harmonics modules:
```python
from harmonics.core import notes
from harmonics.generation import cantus
```

## Testing

### Writing Tests

- Place tests in `tests/` directory
- Name test files as `test_<module>.py`
- Use pytest fixtures for common setup
- Aim for high code coverage (>80%)

Example test:
```python
import pytest
from harmonics.core import notes

def test_note_creation():
    """Test Note class instantiation."""
    note = notes.Note("C", octave=4)
    assert note.pitch == "C"
    assert note.octave == 4

def test_invalid_note():
    """Test that invalid notes raise errors."""
    with pytest.raises(ValueError):
        notes.Note("H")  # Invalid note name
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=harmonics --cov-report=html

# Run specific test file
pytest tests/test_notes.py

# Run specific test
pytest tests/test_notes.py::test_note_creation
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def function(arg1: int, arg2: str) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
        
    Example:
        >>> function(1, "test")
        True
    """
```

### Adding Examples

- Add usage examples in docstrings
- Create Jupyter notebooks in `examples/` directory
- Update README.md if adding major features

## Project Architecture

### Module Organization

```
harmonics/
├── core/           # Pure music theory (no external ML deps)
├── generation/     # Algorithmic composition
├── processing/     # Audio/MIDI I/O
├── ml/            # Machine learning (optional deps)
├── cli/           # Command-line interfaces
└── symbols/       # Abstract musical objects
```

### Design Principles

1. **Modularity**: Keep modules loosely coupled
2. **Optional Dependencies**: Core functionality should work without ML libraries
3. **Type Safety**: Use type hints throughout
4. **Error Handling**: Provide clear error messages
5. **Performance**: Consider performance for large datasets

## Submitting Pull Requests

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Docstrings added/updated
- [ ] README updated (if needed)
- [ ] CHANGELOG.md updated (if applicable)

### PR Description

Include:
- **What**: Brief description of changes
- **Why**: Motivation for the changes
- **How**: Overview of implementation approach
- **Testing**: How you tested the changes

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

## Types of Contributions

### Bug Reports

When reporting bugs, include:
- Python version
- Harmonics version
- Minimal code to reproduce
- Expected vs actual behavior
- Full error traceback

### Feature Requests

When proposing features:
- Describe the use case
- Explain why it's valuable
- Consider implementation approach
- Note any breaking changes

### Good First Issues

Look for issues tagged with:
- `good-first-issue`: Good for newcomers
- `help-wanted`: Areas needing assistance
- `documentation`: Documentation improvements

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on what's best for the community
- Show empathy toward others

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks
- Publishing private information
- Other unprofessional conduct

## Questions?

- Open an issue for discussion
- Check existing issues/PRs first
- Join community discussions

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0-or-later license.

---

Thank you for contributing to Harmonics! 🎵

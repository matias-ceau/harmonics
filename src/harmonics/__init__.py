"""
Harmonics: Music Analysis and Creation Library

A comprehensive Python library for music theory, analysis, and algorithmic composition.

Main modules:
- core: Fundamental music theory objects (notes, scales, chords, intervals)
- generation: Algorithmic composition tools (evolutionary, rule-based)
- processing: Audio and MIDI processing capabilities
- ml: Machine learning models for music generation
- cli: Command line interfaces

Legacy modules (deprecated, use new structure):
- audio, midi: Use processing.audio, processing.midi instead
- data: Use core instead
- theory: Use generation instead
"""

# New organized structure
from . import core
from . import generation
from . import processing
from . import ml
from . import cli

# Legacy imports for backward compatibility
from . import audio
from . import bass  
from . import cadence
from . import data
from . import groove
from . import melody
from . import midi
from . import bot
from . import symbols
from . import synth
from . import theory
from . import _utils

# Re-export symbols for convenience
from .symbols import *

__version__ = "0.1.0"

__all__ = [
    # New structure
    "core",
    "generation", 
    "processing",
    "ml",
    "cli",
    # Legacy modules
    "audio",
    "bass",
    "cadence", 
    "data",
    "groove",
    "melody",
    "midi",
    "bot",
    "symbols",
    "synth",
    "theory",
    "_utils"
]

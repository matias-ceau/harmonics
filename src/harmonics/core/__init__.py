
"""
Core music theory and abstract musical objects.

This module contains the fundamental building blocks for music representation:
- Notes, intervals, chords
- Scales and modes
- Abstract musical containers and data structures
"""

from . import notes
from . import intervals
from . import scales
from . import chords
from . import general
from . import drums
from . import patterns
from . import midi

__all__ = [
    "notes",
    "intervals", 
    "scales",
    "chords",
    "general",
    "drums",
    "patterns",
    "midi"
]

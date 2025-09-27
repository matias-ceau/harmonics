"""
Music generation algorithms and tools.

This module contains various approaches to algorithmic composition:
- Rule-based generation (counterpoint, cantus firmus)  
- Evolutionary algorithms
- Pattern-based generation
"""

from . import cantus
from . import voice
from . import functions

__all__ = [
    "cantus",
    "voice", 
    "functions"
]
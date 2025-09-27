"""
Command line interfaces for harmonics tools.

This module provides CLI access to:
- Music generation tools
- Audio processing utilities  
- Model training and inference
"""

from . import generate
from . import train
from . import analyze

__all__ = [
    "generate",
    "train",
    "analyze"
]
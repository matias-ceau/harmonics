"""
Audio and MIDI processing capabilities.

This module handles:
- Audio analysis and synthesis
- MIDI import/export and manipulation
- Real-time audio processing
"""

from . import audio
from . import midi

__all__ = [
    "audio",
    "midi"
]
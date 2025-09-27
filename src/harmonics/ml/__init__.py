"""
Machine learning components for music generation.

This module contains:
- Neural network models for sequence generation
- Training utilities and data preparation
- Pre-trained model interfaces

Note: Requires torch and transformers packages for ML functionality.
"""

try:
    from .models import MusicGenerationModel, GPT2MusicModel
    from .training import MusicDataset, MusicTrainer
    from .generation import generate_sequence, MusicGenerator
    
    __all__ = [
        "MusicGenerationModel",
        "GPT2MusicModel", 
        "MusicDataset",
        "MusicTrainer",
        "generate_sequence",
        "MusicGenerator"
    ]
except ImportError as e:
    import warnings
    warnings.warn(
        f"ML components not available: {e}. Install with: pip install harmonics[ml]",
        ImportWarning
    )
    __all__ = []
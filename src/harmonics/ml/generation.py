"""
Music generation using trained models.

This module provides high-level interfaces for generating music
using various trained models.
"""

from typing import Optional, Dict, Any
import logging
from .models import GPT2MusicModel

logger = logging.getLogger(__name__)


def generate_sequence(prompt: str, 
                     temperature: float,
                     model_path: Optional[str] = None,
                     max_length: int = 1000,
                     num_return_sequences: int = 1,
                     top_p: float = 1.0,
                     top_k: int = 0) -> str:
    """
    Generate a music sequence using a trained model.
    
    Args:
        prompt: Starting prompt for generation
        temperature: Sampling temperature (0.0 to 1.0)
        model_path: Path to trained model (if None, uses default)
        max_length: Maximum sequence length
        num_return_sequences: Number of sequences to generate
        top_p: Top-p sampling parameter
        top_k: Top-k sampling parameter
    
    Returns:
        Generated sequence as string
    """
    if model_path is None:
        raise ValueError("Model path must be provided")
    
    try:
        model = GPT2MusicModel(model_path)
        return model.generate(
            prompt=prompt,
            temperature=temperature,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            top_p=top_p,
            top_k=top_k
        )
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise


class MusicGenerator:
    """High-level interface for music generation."""
    
    def __init__(self, model_path: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the generator.
        
        Args:
            model_path: Path to trained model
            config: Generation configuration
        """
        self.model_path = model_path
        self.config = config or {}
        self.model = None
        
    def load(self) -> None:
        """Load the model."""
        self.model = GPT2MusicModel(self.model_path)
        
    def generate(self, prompt: str = "^", **kwargs) -> str:
        """
        Generate music from a prompt.
        
        Args:
            prompt: Starting prompt (default: "^" for song start)
            **kwargs: Additional generation parameters
        
        Returns:
            Generated sequence
        """
        if self.model is None:
            self.load()
            
        # Merge config with kwargs
        params = {**self.config, **kwargs}
        
        return self.model.generate(prompt, **params)
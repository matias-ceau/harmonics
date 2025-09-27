"""
Command line interface for music generation.

This module provides CLI access to various music generation algorithms.
"""

import sys
import argparse
import logging
from typing import Optional
from pathlib import Path

try:
    from ..ml.generation import MusicGenerator
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
from ..generation.cantus import run_evolution

logger = logging.getLogger(__name__)


def generate_ml_sequence(args: argparse.Namespace) -> None:
    """Generate sequence using ML models."""
    if not ML_AVAILABLE:
        logger.error("ML functionality not available. Install with: pip install harmonics[ml]")
        sys.exit(1)
        
    try:
        generator = MusicGenerator(args.model_path)
        result = generator.generate(
            prompt=args.prompt,
            temperature=args.temperature,
            max_length=args.max_length
        )
        print(result)
    except Exception as e:
        logger.error(f"ML generation failed: {e}")
        sys.exit(1)


def generate_cantus_firmus(args: argparse.Namespace) -> None:
    """Generate cantus firmus using evolutionary algorithm."""
    try:
        population, generations = run_evolution(
            sequence_length=args.length,
            key_center=args.key,
            population_size=args.population_size,
            generation_limit=args.generations
        )
        
        # Get the best sequence
        best_sequence = population[0] if population else None
        if best_sequence is not None:
            print(" ".join(map(str, best_sequence)))
        else:
            print("No valid sequence generated")
            
    except Exception as e:
        logger.error(f"Cantus firmus generation failed: {e}")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate music using various algorithms"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Generation commands')
    
    # ML generation subcommand
    ml_parser = subparsers.add_parser('ml', help='Generate using ML models')
    ml_parser.add_argument('--model-path', required=True,
                          help='Path to trained model')
    ml_parser.add_argument('--prompt', default='^',
                          help='Generation prompt (default: "^")')
    ml_parser.add_argument('--temperature', type=float, default=0.7,
                          help='Sampling temperature (default: 0.7)')
    ml_parser.add_argument('--max-length', type=int, default=1000,
                          help='Maximum sequence length (default: 1000)')
    ml_parser.set_defaults(func=generate_ml_sequence)
    
    # Cantus firmus generation subcommand
    cantus_parser = subparsers.add_parser('cantus', help='Generate cantus firmus')
    cantus_parser.add_argument('--length', type=int, default=16,
                              help='Sequence length (default: 16)')
    cantus_parser.add_argument('--key', type=int, default=60,
                              help='Key center (MIDI note, default: 60)')
    cantus_parser.add_argument('--population-size', type=int, default=20,
                              help='Population size (default: 20)')
    cantus_parser.add_argument('--generations', type=int, default=1000,
                              help='Maximum generations (default: 1000)')
    cantus_parser.set_defaults(func=generate_cantus_firmus)
    
    # Parse arguments and dispatch
    args = parser.parse_args()
    
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Call appropriate function
    args.func(args)


if __name__ == '__main__':
    main()
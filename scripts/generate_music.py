#!/usr/bin/env python3
"""
Modern replacement for generate_sequence.py

Usage:
    python scripts/generate_music.py --model-path ./results --prompt "^" --temperature 0.7
"""

import sys
import argparse
import logging
from pathlib import Path

# Add src to path so we can import harmonics
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from harmonics.ml.generation import MusicGenerator

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Generate music sequences using trained models"
    )
    parser.add_argument(
        "--model-path", 
        required=True,
        help="Path to trained model directory"
    )
    parser.add_argument(
        "--prompt", 
        default="^",
        help="Generation prompt (default: '^' for song start)"
    )
    parser.add_argument(
        "--temperature", 
        type=float, 
        default=0.7,
        help="Sampling temperature (default: 0.7)"
    )
    parser.add_argument(
        "--max-length", 
        type=int, 
        default=1000,
        help="Maximum sequence length (default: 1000)"
    )
    parser.add_argument(
        "--output-file",
        help="Save output to file instead of printing"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Generate sequence
        generator = MusicGenerator(args.model_path)
        result = generator.generate(
            prompt=args.prompt,
            temperature=args.temperature,
            max_length=args.max_length
        )
        
        # Output result
        if args.output_file:
            with open(args.output_file, 'w') as f:
                f.write(result)
            logger.info(f"Generated sequence saved to {args.output_file}")
        else:
            print(result)
            
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
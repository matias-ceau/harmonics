#!/usr/bin/env python3
"""
Modern replacement for trainer.py

Usage:
    python scripts/train_model.py --tokens tokens.pt --output-dir ./results --epochs 10
"""

import sys
import argparse
import logging
from pathlib import Path
import torch

# Add src to path so we can import harmonics
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from harmonics.ml.training import MusicTrainer, MusicDataset

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Train music generation models"
    )
    parser.add_argument(
        "--tokens", 
        required=True,
        help="Path to tokenized training data (.pt file)"
    )
    parser.add_argument(
        "--output-dir", 
        default="./results",
        help="Output directory for model (default: ./results)"
    )
    parser.add_argument(
        "--model-name", 
        default="gpt2",
        help="Base model name (default: gpt2)"
    )
    parser.add_argument(
        "--epochs", 
        type=int, 
        default=10,
        help="Number of training epochs (default: 10)"
    )
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=1,
        help="Batch size (default: 1)"
    )
    parser.add_argument(
        "--learning-rate", 
        type=float, 
        default=5e-5,
        help="Learning rate (default: 5e-5)"
    )
    parser.add_argument(
        "--seq-length", 
        type=int, 
        default=1024,
        help="Sequence length (default: 1024)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Load tokens
        tokens_path = Path(args.tokens)
        if not tokens_path.exists():
            logger.error(f"Tokens file not found: {tokens_path}")
            sys.exit(1)
        
        tokens = torch.load(tokens_path)
        dataset = MusicDataset(tokens, seq_length=args.seq_length)
        
        # Setup training config
        config = {
            'num_train_epochs': args.epochs,
            'per_device_train_batch_size': args.batch_size,
            'learning_rate': args.learning_rate,
        }
        
        # Create trainer and train
        trainer = MusicTrainer(
            model_name=args.model_name,
            checkpoint_dir=args.output_dir,
            config=config
        )
        
        trainer.train(dataset)
        logger.info("Training completed successfully")
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
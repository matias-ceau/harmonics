"""
Command line interface for model training.

This module provides CLI access to training music generation models.
"""

import sys
import argparse
import logging
from pathlib import Path

try:
    import torch
    from ..ml.training import MusicTrainer, MusicDataset
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

logger = logging.getLogger(__name__)


def train_ml_model(args: argparse.Namespace) -> None:
    """Train ML model from tokens file."""
    if not ML_AVAILABLE:
        logger.error("ML functionality not available. Install with: pip install harmonics[ml]")
        sys.exit(1)
        
    try:
        # Load tokens
        if not Path(args.tokens_path).exists():
            logger.error(f"Tokens file not found: {args.tokens_path}")
            sys.exit(1)
        
        tokens = torch.load(args.tokens_path)
        dataset = MusicDataset(tokens, seq_length=args.seq_length)
        
        # Setup training config
        config = {
            'num_train_epochs': args.epochs,
            'per_device_train_batch_size': args.batch_size,
            'gradient_accumulation_steps': args.grad_accumulation,
            'save_steps': args.save_steps,
            'learning_rate': args.learning_rate,
            'warmup_steps': args.warmup_steps
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


def main() -> None:
    """Main CLI entry point for training."""
    parser = argparse.ArgumentParser(
        description="Train music generation models"
    )
    
    parser.add_argument('--tokens-path', required=True,
                       help='Path to tokenized training data (.pt file)')
    parser.add_argument('--output-dir', default='./results',
                       help='Output directory for model (default: ./results)')
    parser.add_argument('--model-name', default='gpt2',
                       help='Base model name (default: gpt2)')
    parser.add_argument('--seq-length', type=int, default=1024,
                       help='Sequence length (default: 1024)')
    parser.add_argument('--epochs', type=int, default=10,
                       help='Number of training epochs (default: 10)')
    parser.add_argument('--batch-size', type=int, default=1,
                       help='Batch size (default: 1)')
    parser.add_argument('--grad-accumulation', type=int, default=4,
                       help='Gradient accumulation steps (default: 4)')
    parser.add_argument('--save-steps', type=int, default=10000,
                       help='Save checkpoint every N steps (default: 10000)')
    parser.add_argument('--learning-rate', type=float, default=5e-5,
                       help='Learning rate (default: 5e-5)')
    parser.add_argument('--warmup-steps', type=int, default=500,
                       help='Warmup steps (default: 500)')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Train model
    train_ml_model(args)


if __name__ == '__main__':
    main()
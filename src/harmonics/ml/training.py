"""
Training utilities for music generation models.

This module provides:
- Dataset classes for music data
- Training configuration and utilities
- Model checkpointing and resumption
"""

import os
from typing import Dict, Any, Optional
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
import logging

logger = logging.getLogger(__name__)


class MusicDataset(Dataset):
    """Dataset class for music sequence data."""
    
    def __init__(self, tokens: Dict[str, torch.Tensor], seq_length: int = 1024):
        """
        Initialize the dataset.
        
        Args:
            tokens: Dictionary containing 'input_ids' and 'attention_mask' tensors
            seq_length: Length of sequences to create
        """
        self.input_ids = tokens['input_ids']
        self.attn_masks = tokens['attention_mask']
        self.seq_length = seq_length

    def __len__(self) -> int:
        return self.input_ids.shape[1] // self.seq_length

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        start_idx = idx * self.seq_length
        end_idx = start_idx + self.seq_length
        
        input_ids = self.input_ids[:, start_idx:end_idx]
        attention_mask = self.attn_masks[:, start_idx:end_idx]
        labels = input_ids.clone()
        
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }


class MusicTrainer:
    """Trainer class for music generation models."""
    
    def __init__(self, 
                 model_name: str = 'gpt2',
                 checkpoint_dir: str = './results',
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the trainer.
        
        Args:
            model_name: Name or path of the base model
            checkpoint_dir: Directory for saving checkpoints
            config: Training configuration dictionary
        """
        self.model_name = model_name
        self.checkpoint_dir = checkpoint_dir
        self.config = config or self._default_config()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def _default_config(self) -> Dict[str, Any]:
        """Get default training configuration."""
        return {
            'num_train_epochs': 10,
            'per_device_train_batch_size': 1,
            'gradient_accumulation_steps': 4,
            'save_steps': 10000,
            'save_total_limit': 2,
            'logging_steps': 200,
            'eval_steps': 1000,
            'learning_rate': 5e-5,
            'warmup_steps': 500,
            'fp16': True
        }
    
    def load_or_create_model(self) -> tuple[GPT2LMHeadModel, GPT2Tokenizer]:
        """Load existing model or create new one."""
        if os.path.exists(self.checkpoint_dir) and any(os.scandir(self.checkpoint_dir)):
            logger.info(f"Loading model from checkpoint: {self.checkpoint_dir}")
            model = GPT2LMHeadModel.from_pretrained(self.checkpoint_dir)
            tokenizer = GPT2Tokenizer.from_pretrained(self.checkpoint_dir)
        else:
            logger.info(f"Creating new model from: {self.model_name}")
            model = GPT2LMHeadModel.from_pretrained(self.model_name)
            tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        
        # Set pad token
        tokenizer.pad_token_id = tokenizer.eos_token_id
        model.to(self.device)
        
        return model, tokenizer
    
    def train(self, dataset: MusicDataset) -> None:
        """Train the model on the provided dataset."""
        model, tokenizer = self.load_or_create_model()
        
        # Setup training arguments
        training_args = TrainingArguments(
            output_dir=self.checkpoint_dir,
            num_train_epochs=self.config['num_train_epochs'],
            per_device_train_batch_size=self.config['per_device_train_batch_size'],
            gradient_accumulation_steps=self.config['gradient_accumulation_steps'],
            save_steps=self.config['save_steps'],
            save_total_limit=self.config['save_total_limit'],
            logging_dir='./logs',
            logging_steps=self.config['logging_steps'],
            eval_strategy="steps",
            eval_steps=self.config['eval_steps'],
            logging_first_step=True,
            load_best_model_at_end=True,
            report_to="tensorboard",
            fp16=self.config['fp16'],
            learning_rate=self.config['learning_rate'],
            lr_scheduler_type='linear',
            warmup_steps=self.config['warmup_steps']
        )
        
        # Create trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            eval_dataset=dataset  # Use validation set if available
        )
        
        # Check for existing trainer state
        trainer_state_path = os.path.join(self.checkpoint_dir, 'trainer_state.json')
        if os.path.exists(trainer_state_path):
            logger.info(f"Resuming training from {self.checkpoint_dir}")
            trainer.train(resume_from_checkpoint=self.checkpoint_dir)
        else:
            logger.info("Starting new training session")
            trainer.train()
        
        # Save final model
        model.save_pretrained(self.checkpoint_dir)
        tokenizer.save_pretrained(self.checkpoint_dir)
        trainer.state.save_to_json(trainer_state_path)
        
        logger.info("Training complete. Model saved.")
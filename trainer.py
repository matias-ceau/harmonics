import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset, DataLoader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the dataset class
class DrumDataset(Dataset):
    def __init__(self, tokens, seq_length=1024):
        self.input_ids = tokens['input_ids']
        self.attn_masks = tokens['attention_mask']
        self.seq_length = seq_length

    def __len__(self):
        return self.input_ids.shape[1] // self.seq_length

    def __getitem__(self, idx):
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

def main():
    # Load tokens
    tokens_path = 'tokens.pt'
    if not os.path.exists(tokens_path):
        logger.error(f"Tokens file not found: {tokens_path}")
        return

    tokens = torch.load(tokens_path)
    model_name = 'gpt2'
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    # Check for existing model checkpoint
    checkpoint_dir = '/home/matias/git/harmonics/results'
    if os.path.exists(checkpoint_dir) and any(os.scandir(checkpoint_dir)):
        logger.info(f"Resuming from checkpoint in {checkpoint_dir}")
        model = GPT2LMHeadModel.from_pretrained(checkpoint_dir)
        tokenizer = GPT2Tokenizer.from_pretrained(checkpoint_dir)
    else:
        logger.info(f"No checkpoint found. Starting training from scratch.")
        model = GPT2LMHeadModel.from_pretrained(model_name)

    # Ensure the model is moved to GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Set pad token ID to eos token ID
    tokenizer.pad_token_id = tokenizer.eos_token_id

    # Create a Dataset object
    dataset = DrumDataset(tokens)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=checkpoint_dir,
        num_train_epochs=10000,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir='./logs',
        logging_steps=200,
        eval_strategy="steps",
        eval_steps=1000,
        logging_first_step=True,
        load_best_model_at_end=True,
        report_to="tensorboard",
        fp16=True,
        learning_rate=5e-5,
        lr_scheduler_type='linear',
        warmup_steps=500
    )

    # Define the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=dataset,  # Use a separate validation set if available
    )

    # Check for existing trainer state to resume from checkpoint
    if os.path.exists(os.path.join(checkpoint_dir, 'trainer_state.json')):
        logger.info(f"Loading trainer state from {checkpoint_dir}")
        trainer.train(resume_from_checkpoint=checkpoint_dir)
    else:
        logger.info("No trainer state found. Starting new training.")
        trainer.train()

    # Save the model and tokenizer
    model.save_pretrained(checkpoint_dir)
    tokenizer.save_pretrained(checkpoint_dir)

    # Save the training state
    trainer.state.save_to_json(os.path.join(checkpoint_dir, 'trainer_state.json'))

    logger.info("Training complete. Model and state saved.")

if __name__ == "__main__":
    main()

import sys
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_sequence(prompt,
                      temperature,
                      max_length=1000, 
                      num_return_sequences=1, 
                      top_p=1,
                      top_k=0):
    # Load the tokenizer and model
    model_name_or_path = '/home/matias/git/harmonics/results'
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
    model = GPT2LMHeadModel.from_pretrained(model_name_or_path)

    # Ensure the model is moved to GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)

    # Create attention mask for the input
    attention_mask = torch.ones(input_ids.shape, device=device)

    # Generate the sequence
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        do_sample=True,
        top_p=top_p,
        top_k=top_k,
        temperature=temperature
    )

    # Decode the generated sequence
    generated_sequence = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_sequence

def main(prompt=None, temperature=None):
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    elif prompt:
        prompt = prompt
    else:
        prompt = "^"  # Starting symbol for a song
    if temperature:
        temperature = temperature
    else:
        temperature = 0.7
    generated_sequence = generate_sequence(prompt,temperature)
    print(generated_sequence)
    return generated_sequence

if __name__ == "__main__":
    main()

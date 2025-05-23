# -*- coding: utf-8 -*-
"""TrumpTuring5.2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nxJMpo91UtI2HA9kGHYLig4gyRj9pmpq
"""

!pip install -q transformers datasets accelerate peft bitsandbytes sentencepiece huggingface_hub
!pip install -q pandas numpy tqdm
!pip install -U bitsandbytes

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from huggingface_hub import login
import os

from google.colab import drive
drive.mount('/content/drive')

hf_token = input("Enter your Hugging Face token: ")
login(token=hf_token)

# Configure quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Loading base model
print("Loading base model...")
base_model_id = "meta-llama/Llama-2-7b-chat-hf"
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    quantization_config=bnb_config,
    device_map="auto",
    token=hf_token
)

# Loading tokenizer
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(base_model_id, token=hf_token)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


adapter_path = "/content/drive/MyDrive/trump_tweet_model"
print(f"Loading adapter from {adapter_path}...")
try:
    model = PeftModel.from_pretrained(base_model, adapter_path)
    print("Trump tweet generator model loaded successfully!")
except Exception as e:
    print(f"Error loading adapter: {e}")
    print("Trying alternative loading method...")
    try:
        # Alternative loading approach
        from peft import LoraConfig, get_peft_model

        # Temporary LoRA config
        lora_config = LoraConfig(
            r=16,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )

        # Attempt to load as a directory of weights
        model = get_peft_model(base_model, lora_config)
        model.load_state_dict(torch.load(f"{adapter_path}/adapter_model.bin"))
        print("Model loaded with alternative method!")
    except Exception as e2:
        print(f"Alternative loading also failed: {e2}")
        print("Please check your model path and adapter files.")

# Test the model
def generate_trump_tweet(topic, max_length=150):
    """Generate a tweet in Trump's style on a given topic"""
    prompt = f"Generate a tweet in Donald Trump's style about {topic}:"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=150,
            temperature=0.9,
            top_p=0.92,
            top_k=50,
            repetition_penalty=1.2,
            do_sample=True,
            num_return_sequences=1,
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    tweet = generated_text.replace(prompt, "").strip()
    return tweet

print("\nTesting the model with sample topics...")
test_topics = ["the economy", "fake news", "immigration"]
for topic in test_topics:
    try:
        tweet = generate_trump_tweet(topic)
        print(f"Topic: {topic}")
        print(f"Tweet: {tweet}")
        print("-" * 50)
    except Exception as e:
        print(f"Error generating tweet on topic '{topic}': {e}")

# Function to generate tweets interactively
def interactive_tweet_generator():
    while True:
        topic = input("\nEnter a topic for a Trump-style tweet (or 'quit' to exit): ")
        if topic.lower() == 'quit':
            break

        try:
            tweet = generate_trump_tweet(topic)
            print(f"\nGenerated Trump-style tweet about '{topic}':")
            print("-" * 50)
            print(tweet)
            print("-" * 50)
        except Exception as e:
            print(f"Error generating tweet: {e}")

print("\nStarting interactive tweet generator...")
interactive_tweet_generator()
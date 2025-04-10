# core/llm.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hugging Face API config
HUGGINGFACE_API_KEY = os.getenv("HF_API_TOKEN")
MODEL = os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-large")

API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def query_llm(prompt: str, session_id: str = None) -> str:
    """Sends a prompt to Hugging Face model and returns the generated text."""
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        output = response.json()

        # Handle different output formats
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        elif isinstance(output, dict) and "generated_text" in output:
            return output["generated_text"]
        else:
            return str(output)
    except requests.exceptions.RequestException as e:
        return f"❌ HuggingFace API Error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

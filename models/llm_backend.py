# models/llm_backend.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
LLAMA_MODEL_ID = "meta-llama/llama-4-maverick"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

API_URL = f"https://api-inference.huggingface.co/models/{LLAMA_MODEL_ID}"

def call_llama_api(prompt: str, max_tokens: int = 256) -> str:
    """
    Sends a prompt to the LLaMA 4 Maverick model and returns the generated text.
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()

        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            return f"API Error: {result['error']}"
        else:
            return "No valid response from LLaMA API."

    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"


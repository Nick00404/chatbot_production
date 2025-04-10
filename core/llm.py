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
    """
    Sends a prompt to the Hugging Face model and returns the generated text.
    Includes fallback handling for API rate limits and model loading times.
    """
    payload = {"inputs": prompt}

    try:
        # Optional debug logging
        if session_id:
            print(f"[LLM] Session: {session_id} | Prompt: {prompt[:60]}...")

        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()
        output = response.json()

        # Handle model loading or estimated time response
        if isinstance(output, dict) and "estimated_time" in output:
            return "⏳ Model is loading, please try again shortly."

        # Standard output format from HF
        if isinstance(output, list) and output and "generated_text" in output[0]:
            return output[0]["generated_text"]
        elif isinstance(output, dict) and "generated_text" in output:
            return output["generated_text"]

        # Unknown format fallback
        return f"⚠️ Unexpected output: {output}"

    except requests.exceptions.Timeout:
        return "⏰ The request to the language model timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"❌ HuggingFace API Error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

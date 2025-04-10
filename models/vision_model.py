# models/vision_model.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
VISION_MODEL_ID = "Salesforce/blip-image-captioning-base"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

API_URL = f"https://api-inference.huggingface.co/models/{VISION_MODEL_ID}"

def run_image_captioning(image_bytes: bytes) -> str:
    """
    Sends an image to Hugging Face BLIP model for caption generation.
    Returns the generated caption as a string.
    """
    try:
        response = requests.post(API_URL, headers=HEADERS, files={"file": image_bytes})
        response.raise_for_status()

        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            return f"API Error: {result['error']}"
        else:
            return "Unexpected response from vision model."

    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"

# core/vision.py

import requests
import os
from dotenv import load_dotenv
from typing import Optional
from models.vision_model import run_image_captioning


# Load environment variables
load_dotenv()

# Hugging Face API key from .env
HF_API_KEY = os.getenv("HF_API_KEY")

# Use a lightweight vision model for image captioning
HF_VISION_MODEL = "nlpconnect/vit-gpt2-image-captioning"

def generate_caption(image_path: str) -> Optional[str]:
    """
    Sends image to Hugging Face image captioning model and returns a caption.

    Args:
        image_path (str): Local path to the image file.

    Returns:
        str: Caption generated by the model, or error message.
    """
    if not HF_API_KEY:
        return "Hugging Face API key is not set in environment variables."

    api_url = f"https://api-inference.huggingface.co/models/{HF_VISION_MODEL}"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = requests.post(api_url, headers=headers, data=image_bytes)

        if response.status_code == 503:
            return "Model is loading. Please try again in a few seconds."
        elif response.status_code != 200:
            return f"Error from Hugging Face API: {response.status_code} - {response.text}"

        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        return "No caption returned by the model."

    except Exception as e:
        return f"Error during caption generation: {str(e)}"

class VisionModel:
    def __init__(self):
        pass  # You can later load models or settings here if needed

    def generate_caption(self, image_path):
        return run_image_captioning(image_path)
    

analyze_image = generate_caption

def generate_caption(image_path):
    return run_image_captioning(image_path)
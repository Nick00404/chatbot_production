# core/vision.py

import os
import requests
from dotenv import load_dotenv
from typing import Optional
from models.vision_model import run_image_captioning

# Load environment variables
load_dotenv()

# Hugging Face API details
HF_API_KEY = os.getenv("HF_API_KEY")
HF_VISION_MODEL = "nlpconnect/vit-gpt2-image-captioning"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_VISION_MODEL}"

def generate_caption(image_path: str, use_api: bool = True) -> str:
    """
    Generates a caption for an image using either Hugging Face API or a local model.

    Args:
        image_path (str): Path to the image file.
        use_api (bool): Whether to use the Hugging Face API. If False or unavailable, local model is used.

    Returns:
        str: Generated caption or error message.
    """
    if use_api and HF_API_KEY:
        try:
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()

            response = requests.post(
                HF_API_URL,
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                data=image_bytes,
                timeout=10
            )

            if response.status_code == 503:
                return "⏳ Model is loading. Please try again shortly."
            elif response.status_code != 200:
                return f"❌ API Error: {response.status_code} - {response.text}"

            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            return "⚠️ Unexpected API response format."

        except Exception as e:
            return f"❌ Error calling Hugging Face API: {str(e)}"

    # Fallback: local model
    try:
        return run_image_captioning(image_path)
    except Exception as e:
        return f"❌ Local model error: {str(e)}"

class VisionModel:
    def __init__(self, use_api=True):
        self.use_api = use_api

    def generate_caption(self, image_path: str) -> str:
        return generate_caption(image_path, use_api=self.use_api)

# Aliases
analyze_image = generate_caption

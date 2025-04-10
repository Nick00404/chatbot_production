# core/vision.py

import os
import requests
from dotenv import load_dotenv


load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


class VisionModel:
    def __init__(self):
        pass

    def predict(self, image_file):
        # Save the uploaded image temporarily
        upload_dir = os.path.join(os.getcwd(), "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        image_path = os.path.join(upload_dir, image_file.filename)
        image_file.save(image_path)

        # Read image in binary format
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Send request to Hugging Face API
        response = requests.post(API_URL, headers=HEADERS, data=image_bytes)

        if response.status_code != 200:
            return f"Error from Hugging Face API: {response.status_code}"

        try:
            result = response.json()
            caption = result[0]["generated_text"]
            return caption
        except Exception:
            return "Failed to parse caption from response."

# routes/chat_multimodal_routes.py

from flask import Blueprint, request, jsonify, session
from core.vision import VisionModel, generate_caption
from core.llm import query_llm
from core.session_handler import save_message_to_session
import uuid
import os

UPLOAD_FOLDER = "uploads"  # Define the folder for saving uploaded images
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the folder if it doesn't exist

chat_multimodal_bp = Blueprint("chat_multimodal", __name__)
vision_model = VisionModel()

@chat_multimodal_bp.route("/chat/multimodal", methods=["POST"])
def chat_multimodal():
    try:
        image = request.files.get("image")
        prompt = request.form.get("prompt", "").strip()
        session_id = session.get("session_id")

        if not image:
            return jsonify({"error": "Image file is missing"}), 400

        if not prompt:
            return jsonify({"error": "Text prompt is missing"}), 400

        # Save image
        try:
            filename = f"{uuid.uuid4().hex}_{image.filename}"
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
        except Exception as e:
            print("Image saving failed:", e)
            return jsonify({"error": "Failed to save image"}), 500

        # Vision captioning
        try:
            caption = generate_caption(image_path)
        except Exception as e:
            print("Vision model error:", e)
            return jsonify({"error": "Failed to generate image caption"}), 500

        # Combine caption and prompt
        multimodal_prompt = f"Image Description: {caption}\nUser Prompt: {prompt}"
        llm_reply = query_llm(multimodal_prompt)

        # Save messages
        if session_id:
            try:
                save_message_to_session(session_id, "user", prompt)
                save_message_to_session(session_id, "bot", llm_reply)
            except Exception as e:
                print("Message saving failed:", e)

        return jsonify({
            "caption": caption,
            "response": llm_reply
        }), 200

    except Exception as e:
        print("Error in /chat/multimodal:", e)
        return jsonify({"error": "An internal error occurred"}), 500


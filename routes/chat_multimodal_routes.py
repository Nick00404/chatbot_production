# chat_multimodal_routes.py

import os
import uuid
from flask import Blueprint, request, jsonify
from core.llm import query_llm
from core.vision import generate_caption
from core.session_handler import save_message, get_active_session
from core.auth import verify_token

chat_bp = Blueprint("chat", __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_current_user():
    """Centralized auth checker"""
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None
    return verify_token(token.split(" ")[1])

@chat_bp.route("/", methods=["POST"])
def chat():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not (message := data.get("message")):
        return jsonify({"error": "Message required"}), 400

    try:
        response = query_llm(message)
        if session_id := get_active_session(user["id"]):
            save_message(session_id, "user", message)
            save_message(session_id, "bot", response)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat_bp.route("/multimodal", methods=["POST"])
def multimodal_chat():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if not (image := request.files.get("image")):
        return jsonify({"error": "Image required"}), 400
    
    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt required"}), 400

    try:
        filename = f"{uuid.uuid4().hex}_{image.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
        
        caption = generate_caption(image_path)
        response = query_llm(f"Image: {caption}\nPrompt: {prompt}")
        
        if session_id := get_active_session(user["id"]):
            save_message(session_id, "user", prompt)
            save_message(session_id, "bot", response)
            
        os.remove(image_path)  # Cleanup
        return jsonify({"caption": caption, "response": response})
    
    except Exception as e:
        if os.path.exists(image_path):
            os.remove(image_path)
        return jsonify({"error": str(e)}), 500
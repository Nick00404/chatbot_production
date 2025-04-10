from flask import Blueprint, request, jsonify
from core.vision import VisionModel, generate_caption
from core.llm import query_llm
from core.session_handler import save_message_to_session, get_active_session_for_user
from core.auth import verify_token
import uuid
import os

chat_multimodal_bp = Blueprint("chat_multimodal", __name__)
vision_model = VisionModel()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_id():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None
    payload = verify_token(token.split(" ")[1])
    return payload.get("username") if payload else None

@chat_multimodal_bp.route("/api/chat/multimodal", methods=["POST"])
def chat_multimodal():
    try:
        user_id = get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        image = request.files.get("image")
        prompt = request.form.get("prompt", "").strip()

        if not image or not allowed_file(image.filename):
            return jsonify({"error": "Invalid or missing image file"}), 400

        if not prompt:
            return jsonify({"error": "Text prompt is missing"}), 400

        # Save image
        filename = f"{uuid.uuid4().hex}_{image.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            image.save(image_path)
        except Exception as e:
            print("Image saving failed:", e)
            return jsonify({"error": "Failed to save image"}), 500

        # Generate image caption
        try:
            caption = generate_caption(image_path)
        except Exception as e:
            print("Caption generation failed:", e)
            return jsonify({"error": "Failed to generate image caption"}), 500

        # Query LLM
        multimodal_prompt = f"Image Description: {caption}\nUser Prompt: {prompt}"
        try:
            llm_reply = query_llm(multimodal_prompt)
        except Exception as e:
            print("LLM query failed:", e)
            return jsonify({"error": "Failed to get response from LLM"}), 500

        # Save conversation to session (if available)
        try:
            session_id = get_active_session_for_user(user_id)
            if session_id:
                save_message_to_session(session_id, "user", prompt)
                save_message_to_session(session_id, "bot", llm_reply)
        except Exception as e:
            print("Session message saving failed:", e)

        return jsonify({
            "caption": caption,
            "response": llm_reply
        }), 200

    except Exception as e:
        print("Unexpected error in /chat/multimodal:", e)
        return jsonify({"error": "Internal server error"}), 500

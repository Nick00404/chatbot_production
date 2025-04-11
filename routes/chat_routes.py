# routes/chat_routes.py

import os
import uuid
from flask import Blueprint, request, jsonify, session
from core.llm import query_llm
from core.vision import generate_caption
from core.session_handler import save_message
from core.auth import verify_token

chat_bp = Blueprint("chat", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------
# Helper: Auth Wrapper
# -------------------------------
def extract_user_from_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None

    token = token.split(" ")[1]
    return verify_token(token)


# -------------------------------
# Chat (Authenticated)
# -------------------------------
@chat_bp.route("/", methods=["POST"])
def chat():
    payload = extract_user_from_token()
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    message = data.get("message")
    session_id = session.get("session_id")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Query LLM
    llm_response = query_llm(message)

    # Save conversation
    if session_id:
        save_message(session_id, "user", message)
        save_message(session_id, "bot", llm_response)

    return jsonify({"response": llm_response})


# -------------------------------
# Chat Text (No Auth Required)
# -------------------------------
@chat_bp.route("/text", methods=["POST"])
def chat_text():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        session_id = session.get("session_id")

        if not message:
            return jsonify({"error": "Empty message is not allowed"}), 400

        response = query_llm(message)

        if session_id:
            try:
                save_message(session_id, "user", message)
                save_message(session_id, "bot", response)
            except Exception as e:
                print("Warning: failed to save messages", e)

        return jsonify({"response": response}), 200

    except Exception as e:
        print("Internal server error in /chat/text:", e)
        return jsonify({"error": "Internal server error"}), 500


# -------------------------------
# Chat Multimodal (Image + Prompt)
# -------------------------------
@chat_bp.route("/multimodal", methods=["POST"])
def chat_multimodal():
    image = request.files.get("image")
    prompt = request.form.get("prompt", "").strip()
    session_id = session.get("session_id")

    if not image or not prompt:
        return jsonify({"error": "Missing image or prompt"}), 400

    # Save uploaded image
    filename = f"{uuid.uuid4().hex}_{image.filename}"
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    # Analyze image + prompt
    caption = generate_caption(image_path)
    combined_prompt = f"Image Description: {caption}\nUser Prompt: {prompt}"
    response = query_llm(combined_prompt)

    if session_id:
        save_message(session_id, "user", prompt)
        save_message(session_id, "bot", response)

    return jsonify({
        "caption": caption,
        "response": response
    })

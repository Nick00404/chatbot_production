# routes/chat_routes.py
import os
import uuid
from flask import Blueprint, request, jsonify, session
from core import get_llm_response, generate_caption, save_message_to_session


chat_bp = Blueprint("chat", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@chat_bp.route("/chat/text", methods=["POST"])
def chat_text():
    data = request.get_json()
    user_input = data.get("message", "")
    session_id = session.get("session_id")

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    # LLM response
    llm_reply = get_llm_response(user_input)

    # Save to session
    if session_id:
        save_message_to_session(session_id, "user", user_input)
        save_message_to_session(session_id, "bot", llm_reply)

    return jsonify({"response": llm_reply})


@chat_bp.route("/chat/multimodal", methods=["POST"])
def chat_multimodal():
    image = request.files.get("image")
    prompt = request.form.get("prompt", "")
    session_id = session.get("session_id")

    if not image or not prompt:
        return jsonify({"error": "Missing image or prompt"}), 400

    # Save image
    filename = f"{uuid.uuid4().hex}_{image.filename}"
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    # Vision captioning
    caption = generate_caption(image_path)

    # Combine vision + user prompt
    multimodal_prompt = f"Image Description: {caption}\nUser Prompt: {prompt}"
    llm_reply = get_llm_response(multimodal_prompt)

    # Save to session
    if session_id:
        save_message_to_session(session_id, "user", prompt)
        save_message_to_session(session_id, "bot", llm_reply)

    return jsonify({
        "caption": caption,
        "response": llm_reply
    })

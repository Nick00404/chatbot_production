from flask import Blueprint, request, jsonify
from core.llm import generate_llm_response
from core.vision import analyze_image
from core.session_handler import save_message, get_session_messages

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get("session_id")
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Save user message
    save_message(session_id, "user", message)

    # Get response from LLM
    response = generate_llm_response(message)
    save_message(session_id, "bot", response)

    return jsonify({"response": response}), 200


@chat_bp.route('/vision', methods=['POST'])
def vision():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    result = analyze_image(image_file)

    return jsonify({"result": result}), 200


@chat_bp.route('/history/<session_id>', methods=['GET'])
def chat_history(session_id):
    messages = get_session_messages(session_id)
    return jsonify({"messages": messages}), 200

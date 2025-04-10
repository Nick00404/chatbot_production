# routes/chat_multimodal_routes.py

from flask import Blueprint, request, jsonify, session
from core.vision import VisionModel
from core.llm import query_llm

chat_multimodal_bp = Blueprint("chat_multimodal", __name__)
vision_model = VisionModel()

@chat_multimodal_bp.route("/chat/multimodal", methods=["POST"])
def multimodal_chat():
    image = request.files.get("image")
    prompt = request.form.get("prompt")

    if not image or not prompt:
        return jsonify({"error": "Both image and prompt are required."}), 400

    # Step 1: Get image caption
    caption = vision_model.predict(image)

    # Step 2: Combine image description + user prompt
    combined_prompt = f"Image Description: {caption}\nUser Question: {prompt}"

    # Step 3: Query LLM (LLaMA)
    try:
        response = query_llm(combined_prompt)
        return jsonify({"caption": caption, "response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

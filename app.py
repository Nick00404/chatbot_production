import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Blueprints
from routes.chat_multimodal_routes import chat_multimodal_bp
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from routes.session_routes import session_bp

# Import core utilities
from core.llm import query_llm
from core.vision import analyze_image
from core.auth import is_authorized
from core.session_handler import init_db, save_message, get_session_messages, delete_session

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Initialize the database
init_db()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(session_bp, url_prefix="/api/session")
app.register_blueprint(chat_multimodal_bp)
app.register_blueprint(chat_bp)

# ------------------------------
# Routes
# ------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():
    token = request.headers.get("Authorization")
    if not is_authorized(token):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    prompt = data.get("message")
    session_id = data.get("session_id")

    if not prompt:
        return jsonify({"error": "Missing 'message' in request"}), 400
    if not session_id:
        return jsonify({"error": "Missing 'session_id' in request"}), 400

    try:
        save_message(session_id, "user", prompt)
        response = query_llm(prompt, session_id=session_id)
        save_message(session_id, "bot", response)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@app.route("/api/image", methods=["POST"])
def image_upload():
    token = request.headers.get("Authorization")
    if not is_authorized(token):
        return jsonify({"error": "Unauthorized"}), 401

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        result = analyze_image(file.stream)
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": f"Image analysis failed: {str(e)}"}), 500


@app.route("/api/session/<session_id>", methods=["GET"])
def get_session(session_id):
    try:
        messages = get_session_messages(session_id)
        return jsonify({"messages": messages})
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve session: {str(e)}"}), 500


@app.route("/api/session/<session_id>", methods=["DELETE"])
def delete(session_id):
    try:
        delete_session(session_id)
        return jsonify({"status": f"Session '{session_id}' deleted"})
    except Exception as e:
        return jsonify({"error": f"Failed to delete session: {str(e)}"}), 500


@app.route("/")
def index():
    return jsonify({"status": "Running", "message": "Chatbot Backend is live ✅"})


# Run the app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes.chat_multimodal_routes import chat_multimodal_bp
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from routes.session_routes import session_bp

# Load environment variables
load_dotenv()

# Import custom modules
from core.llm import query_llm
from core.vision import analyze_image
from core.auth import is_authorized
from core.session_handler import init_db, save_message, get_session_messages, delete_session

# Import Blueprints
from routes.session_routes import session_routes

# Initialize the Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Initialize database on startup
init_db()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(session_routes, url_prefix="/api/session")
app.register_blueprint(chat_multimodal_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(session_bp)

# Custom endpoints
@app.route("/api/chat", methods=["POST"])
def chat():
    token = request.headers.get("Authorization")
    if not is_authorized(token):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    session_id = data.get("session_id", "default")
    prompt = data.get("message")

    save_message(session_id, "user", prompt)
    response = query_llm(prompt, session_id=session_id)
    save_message(session_id, "bot", response)

    return jsonify({"response": response})

@app.route("/api/image", methods=["POST"])
def image_upload():
    token = request.headers.get("Authorization")
    if not is_authorized(token):
        return jsonify({"error": "Unauthorized"}), 401

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    result = analyze_image(file.stream)
    return jsonify({"response": result})

@app.route("/api/session/<session_id>", methods=["GET"])
def get_session(session_id):
    messages = get_session_messages(session_id)
    return jsonify({"messages": messages})

@app.route("/api/session/<session_id>", methods=["DELETE"])
def delete(session_id):
    delete_session(session_id)
    return jsonify({"status": f"Session '{session_id}' deleted"})

@app.route("/")
def index():
    return jsonify({"status": "Running", "message": "Chatbot Backend is live ✅"})

# Run the app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

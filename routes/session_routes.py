from flask import Blueprint, request, jsonify
from core.session_handler import (
    get_all_sessions,
    create_session,
    delete_session,
    get_sessions_for_user,
    get_session_messages,
)
from core.auth import verify_token

session_bp = Blueprint("sessions", __name__)

# Helper: get user_id from JWT
def get_user_id_from_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None
    payload = verify_token(token.split(" ")[1])
    return payload.get("username") if payload else None


# Create a new session
@session_bp.route("/api/session", methods=["POST"])
def new_session():
    data = request.get_json()
    session_name = data.get("name")
    if not session_name:
        return jsonify({"error": "Session name is required"}), 400

    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    session_id = create_session(user_id, session_name)
    return jsonify({"message": "Session created", "id": session_id}), 201


# List all sessions for user
@session_bp.route("/api/sessions", methods=["GET"])
def list_sessions():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    sessions = get_sessions_for_user(user_id)
    return jsonify(sessions), 200


# Delete a session
@session_bp.route("/api/session/<int:session_id>", methods=["DELETE"])
def remove_session(session_id):
    success = delete_session(session_id)
    if not success:
        return jsonify({"error": "Session not found"}), 404
    return jsonify({"message": "Session deleted"}), 200


# Get messages for a specific session
@session_bp.route("/api/session/<int:session_id>/messages", methods=["GET"])
def get_messages(session_id):
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    messages = get_session_messages(session_id)
    return jsonify({"messages": messages}), 200

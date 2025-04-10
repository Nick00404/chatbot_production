from flask import Blueprint, request, jsonify, session
from core.session_handler import (
    get_all_sessions,
    create_session,
    delete_session,
    get_sessions_for_user,
    get_session_messages,  # now using consistent naming
)

session_bp = Blueprint("sessions", __name__)

# Create new session
@session_bp.route("/api/session", methods=["POST"])
def new_session():
    data = request.json
    session_name = data.get("name")
    if not session_name:
        return jsonify({"error": "Session name is required"}), 400

    # Extract user_id (adjust this based on your auth setup)
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    session_id = create_session(user_id, session_name)
    session["session_id"] = session_id
    return jsonify({"message": "Session created", "id": session_id}), 201

# Get all sessions (optionally for current user)
@session_bp.route("/api/sessions", methods=["GET"])
def list_sessions():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401
    sessions = get_sessions_for_user(user_id)
    return jsonify(sessions), 200

# Delete a session
@session_bp.route("/api/session/<int:session_id>", methods=["DELETE"])
def remove_session(session_id):
    success = delete_session(session_id)
    if not success:
        return jsonify({"error": "Session not found"}), 404
    return jsonify({"message": "Session deleted"}), 200

# Retrieve messages from current session
@session_bp.route("/messages", methods=["GET"])
def get_messages():
    session_id = session.get("session_id")
    if not session_id:
        return jsonify({"error": "No active session"}), 404

    messages = get_session_messages(session_id)
    return jsonify({"messages": messages}), 200

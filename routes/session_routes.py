from flask import Blueprint, request, jsonify, session
from core import (
    get_all_sessions,
    create_session,
    delete_session,
    get_sessions_for_user,
)
session_bp = Blueprint("sessions", __name__)
session_routes = Blueprint("session_routes", __name__)

# Create new session
@session_routes.route("/api/session", methods=["POST"])
def new_session():
    data = request.json
    session_name = data.get("name")
    if not session_name:
        return jsonify({"error": "Session name is required"}), 400
    session_id = create_session(session_name)
    return jsonify({"message": "Session created", "id": session_id}), 201

# Get all sessions
@session_routes.route("/api/sessions", methods=["GET"])
def list_sessions():
    sessions = get_all_sessions()
    return jsonify(sessions), 200

# Delete a session
@session_routes.route("/api/session/<int:session_id>", methods=["DELETE"])
def remove_session(session_id):
    success = delete_session(session_id)
    if not success:
        return jsonify({"error": "Session not found"}), 404
    return jsonify({"message": "Session deleted"}), 200

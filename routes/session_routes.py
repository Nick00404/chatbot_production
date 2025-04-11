# routes/session_routes.py

from flask import Blueprint, request, jsonify
from core.session_handler import (
    get_all_sessions,
    create_session,
    delete_session,
    get_sessions_for_user,
    get_session_messages,
)
from core.auth import verify_token
import sqlite3

session_bp = Blueprint("sessions", __name__, url_prefix="/api/session")


# 🔐 Helper: Extract user ID (username) from token
def get_user_id_from_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    return payload.get("username") if payload else None


# ✅ POST /api/session/ — Create a new chat session
@session_bp.route("/", methods=["POST"])
def new_session():
    data = request.get_json()
    session_name = data.get("name")

    if not session_name:
        return jsonify({"error": "Session name is required"}), 400

    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        session_id = create_session(user_id, session_name)
        return jsonify({"message": "Session created", "id": session_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# routes/session_routes.py
@session_bp.route('/sessions', methods=['GET'])
def list_sessions():
    user_id = get_user_id_from_token()
    try:
        sessions = get_sessions_for_user(user_id)
        return jsonify(sessions), 200
    except (ValueError, sqlite3.Error) as e:
        return jsonify({"error": str(e)}), 400


# ✅ DELETE /api/session/<id> — Delete a session
@session_bp.route("/<int:session_id>", methods=["DELETE"])
def remove_session(session_id):
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        success = delete_session(session_id)
        if not success:
            return jsonify({"error": "Session not found"}), 404
        return jsonify({"message": "Session deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ GET /api/session/<id>/messages — Get all messages in a session
@session_bp.route("/<int:session_id>/messages", methods=["GET"])
def get_messages(session_id):
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        messages = get_session_messages(session_id)
        if messages is None:
            return jsonify({"error": "Session not found"}), 404
        return jsonify({"messages": messages}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

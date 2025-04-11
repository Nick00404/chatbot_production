import jwt
import datetime
import os
from flask import Blueprint, request, jsonify, session
from core import auth
from core.auth import verify_token, create_token
from core.auth import register_user
from core.session_handler import create_session

auth_bp = Blueprint("auth", __name__)

# -----------------------
# Register Route
# -----------------------

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate presence of username and password
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Username and password required"}), 400

    # Attempt to register the user
    success, message = register_user(data['username'], data['password'])

    # Return appropriate response based on success
    status_code = 201 if success else 400
    return jsonify({"message": message}), status_code



# -----------------------
# Login Route
# -----------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400

    success, message = auth.login_user(username, password)
    if success:
        token = create_token(username)  # Use centralized function
        session['session_id'] = create_session(username)

        return jsonify({
            "success": True,
            "message": message,
            "token": token
        }), 200

    return jsonify({"success": False, "message": message}), 401


# ✅ NOTE: Move this to chat_routes.py — leaving here breaks separation of concerns
# Example:
# @chat_bp.route("/", methods=["POST"])
# # def chat(): ...

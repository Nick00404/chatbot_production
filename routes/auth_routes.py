import jwt
import datetime
import os
from flask import Blueprint, request, jsonify
from core import auth
from core.auth import verify_token  # Import the verify_token function

auth_bp = Blueprint("auth", __name__)

# Register route for user registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    success, message = auth.register_user(username, password)
    status = 201 if success else 400
    return jsonify({"success": success, "message": message}), status

# Login route to authenticate the user
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    success, message = auth.login_user(username, password)
    if success:
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            os.getenv("SECRET_KEY", "supersecretkey"),
            algorithm="HS256"
        )
        # ✅ Add this line
        session['session_id'] = create_session(username)

        return jsonify({"success": True, "message": message, "token": token}), 200

    return jsonify({"success": False, "message": message}), 401

# Chat route with token authorization
@auth_bp.route("/api/chat", methods=["POST"])
def chat():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401
    
    token = token.split(" ")[1]  # Extract the token part after "Bearer"
    payload = verify_token(token)  # This assumes verify_token is a function in core.auth
    
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Token is valid, proceed with handling the chat request
    username = payload['username']
    return jsonify({"response": f"Hello, {username}!"})

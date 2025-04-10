# routes/auth_routes.py
from flask import Blueprint, request, jsonify, session
from core import verify_user, hash_password, auth

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    success, message = auth.login_user(username, password)
    status = 200 if success else 401
    return jsonify({"success": success, "message": message}), status

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    success, message = auth.register_user(username, password)
    status = 201 if success else 400
    return jsonify({"success": success, "message": message}), status
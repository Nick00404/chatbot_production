import os
import jwt
import hashlib
import datetime
from flask import request 
from flask import current_app
from functools import wraps
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env into environment

AUTHORIZED_API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
SECRET_KEY = current_app.config.get('SECRET_KEY', 'supersecretkey')


def is_authorized(token):
    try:
        # Remove "Bearer " prefix
        token = token.split(" ")[1] if token.startswith("Bearer ") else token
        
        # Decode the JWT token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Optionally, you can verify that the token has the correct claims (e.g., username, expiration)
        if decoded_token.get("username"):
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    return False


def verify_user(username, password):
    # check user from DB or dummy data
    return True  # or real logic

def hash_password(password):
    # return hashed password string
    return password  # or real hashing

def check_credentials(username, password):
    # Your logic here
    pass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    # Dummy example, should check DB and hash password
    if not username or not password:
        return False, "Username and password required"

    # TODO: Insert user into database
    return True, "User registered successfully"

def login_user(username, password):
    # Dummy logic — replace with real DB check
    if username == "testuser" and password == "password123":
        return True, "Login successful"
    return False, "Invalid credentials"


def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'username': username,
        'exp': expiration_time
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # Return the decoded payload if token is valid
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
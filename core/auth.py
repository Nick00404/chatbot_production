import os
import jwt
import hashlib
import datetime
from flask import current_app
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env into environment

AUTHORIZED_API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

with current_app.app_context():
    SECRET_KEY = current_app.config.get('SECRET_KEY', 'supersecretkey')

def is_authorized(token):
    if not token:
        print("Authorization failed: No token provided.")
        return False

    if not token.startswith("Bearer "):
        print("Authorization failed: Token format incorrect.")
        return False

    actual_token = token.split(" ")[1]
    return actual_token == "expected_token_value"


def verify_user(username, password):
    # Placeholder function; parameters are currently unused
    _ = username
    _ = password
    return True  # or real logic
    # return hashed password string
    return password  # or real hashing

def check_credentials(username, password):
    # Placeholder function; parameters are currently unused
    _ = username
    _ = password
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

    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
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
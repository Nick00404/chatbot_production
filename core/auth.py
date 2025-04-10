import os
import jwt
import hashlib
import datetime
import sqlite3
from flask import current_app
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_PATH = "data/database.sqlite"


def get_secret_key():
    """Safely get the Flask secret key within the app context."""
    try:
        return current_app.config.get("SECRET_KEY", os.getenv("SECRET_KEY", "supersecretkey"))
    except RuntimeError:
        # Fallback if not in app context (for CLI/db scripts)
        return os.getenv("SECRET_KEY", "supersecretkey")


def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def check_credentials(username, password):
    """Check if a user's credentials are valid (DB lookup + password hash match)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False

    stored_hash = row[0]
    return stored_hash == hash_password(password)


def register_user(username, password):
    """Register a new user in the database."""
    if not username or not password:
        return False, "Username and password required"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password)),
        )
        conn.commit()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()


def login_user(username, password):
    """Validate login credentials."""
    if check_credentials(username, password):
        return True, "Login successful"
    return False, "Invalid credentials"


def create_token(username):
    """Create a JWT token for a user."""
    secret_key = get_secret_key()
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'username': username,
        'exp': expiration_time
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def verify_token(token):
    """Decode and verify a JWT token."""
    secret_key = get_secret_key()
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def is_authorized(token):
    """Check if the token exists and matches expected format."""
    if not token:
        print("Authorization failed: No token provided.")
        return False

    if not token.startswith("Bearer "):
        print("Authorization failed: Token format incorrect.")
        return False

    actual_token = token.split(" ")[1]
    decoded = verify_token(actual_token)
    if decoded:
        return True
    else:
        print("Authorization failed: Invalid or expired token.")
        return False

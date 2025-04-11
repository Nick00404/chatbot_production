# tests/helpers.py

# tests/helpers.py (FIXED IMPORTS)
from .conftest import client  # <-- Added dot for relative import
from core.auth import create_token, verify_token
from tests.conftest import client
import jwt
from datetime import datetime, timedelta

def create_test_user(client, username="testuser", password="testpass"):
    """Helper: Register a test user"""
    return client.post('/api/auth/register', json={
        "username": username,
        "password": password
    })
# tests/helpers.py

def get_auth_header(client, username="testuser", password="testpass"):
    """
    Helper function to get a valid JWT token for authentication in tests.

    Args:
        client (FlaskClient): Flask test client instance.
        username (str): Test username.
        password (str): Test password.

    Returns:
        dict: Authorization header with a valid Bearer token.
    """
    # Attempt to register the user (ignore errors like 'user already exists')
    client.post('/api/auth/register', json={
        "username": username,
        "password": password
    })

    # Log in to get JWT token
    login_res = client.post('/api/auth/login', json={
        "username": username,
        "password": password
    })

    # Check for successful login
    assert login_res.status_code == 200, f"Login failed: {login_res.data}"

    # Extract token and return auth header
    token = login_res.json.get("token")
    assert token, f"Token not found in response: {login_res.json}"

    return {'Authorization': f'Bearer {token}'}


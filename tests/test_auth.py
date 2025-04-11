# tests/test_auth.py

from tests.helpers import create_test_user

# tests/test_auth.py
def test_register_user(client):
    """Test successful user registration"""
    # First clear existing users
    client.post('/api/auth/register', json={
        "username": "newuser",
        "password": "securepass"
    })
    
    # Test new registration
    response = client.post('/api/auth/register', json={
        "username": "uniqueuser",
        "password": "securepass"
    })
    assert response.status_code == 201
    assert "success" in response.json['message'].lower()
    
def test_duplicate_registration(client):
    """Test registering same username twice"""
    client.post('/api/auth/register', json={"username": "dupe", "password": "pass"})
    response = client.post('/api/auth/register', json={"username": "dupe", "password": "pass"})
    assert response.status_code == 400
    assert "already exists" in response.json['message'].lower()  # Changed key
    
def test_valid_login(client):
    """Test successful login with correct credentials"""
    create_test_user(client)
    response = client.post('/api/auth/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "token" in response.json

def test_invalid_login(client):
    """Test login with wrong password"""
    create_test_user(client)
    response = client.post('/api/auth/login', json={
        "username": "testuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
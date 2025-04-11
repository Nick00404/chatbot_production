# tests/test_sessions.py

from tests.helpers import get_auth_header
def test_list_sessions(client):
    """Test retrieving user sessions"""
    headers = get_auth_header(client)
    
    # Create 2 test sessions
    client.post('/api/session/', json={"name": "Session 1"}, headers=headers)
    client.post('/api/session/', json={"name": "Session 2"}, headers=headers)
    
    # Get sessions
    response = client.get('/api/session/sessions', headers=headers)
    
    assert response.status_code == 200
    sessions = response.json
    assert len(sessions) == 2
    assert sessions[0]['name'] == "Session 2"  # Ensure reverse chronological order
    assert sessions[1]['name'] == "Session 1"
# tests/test_chat.py

from io import BytesIO 

def get_auth_header(client):
    """Mock function to generate authentication headers."""
    return {"Authorization": "Bearer mock_token"}

class TestTextChat:
    def test_text_chat(self, client, mock_llm):
        """Test basic text chat with mock LLM"""
        headers = get_auth_header(client)
        response = client.post('/api/chat', 
                             json={"message": "Hello"},
                             headers=headers)
        assert response.status_code == 200
        assert "Mock LLM Response" in response.json['response']

class TestMultimodalChat:
    def test_image_chat(self, client, mock_llm, mock_vision):
        """Test image+text chat with mocks"""
        headers = get_auth_header(client)
        data = {
            "image": (BytesIO(b"fake image"), "test.jpg"),
            "prompt": "Describe this"
        }
        response = client.post('/api/chat/multimodal',
                             data=data,
                             headers=headers,
                             content_type='multipart/form-data')
        assert response.status_code == 200
        assert "Mock Image Caption" in response.json['caption']
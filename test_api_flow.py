import requests

BASE_URL = "http://localhost:5000"  # Adjust if you're using a different port

session = requests.Session()

def register_user(username, password):
    res = session.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": password
    })
    print("Register:", res.status_code, res.json())

def login_user(username, password):
    res = session.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    })
    print("Login:", res.status_code, res.json())
    return res.json().get("token")

def create_session(name):
    res = session.post(f"{BASE_URL}/api/session", json={"name": name})
    print("Create Session:", res.status_code, res.json())

def send_text_chat(message):
    res = session.post(f"{BASE_URL}/api/chat/text", json={"message": message})
    print("Text Chat:", res.status_code, res.json())

def send_multimodal_chat(prompt, image_path):
    with open(image_path, "rb") as img_file:
        res = session.post(f"{BASE_URL}/chat/multimodal", data={"prompt": prompt}, files={"image": img_file})
    print("Multimodal Chat:", res.status_code, res.json())

def get_sessions():
    res = session.get(f"{BASE_URL}/api/sessions")
    print("Sessions:", res.status_code, res.json())

def get_messages():
    res = session.get(f"{BASE_URL}/messages")
    print("Messages:", res.status_code, res.json())

if __name__ == "__main__":
    USERNAME = "testuser"
    PASSWORD = "secure123"
    IMAGE_PATH = "example.jpg"  # Make sure this file exists in the same directory

    register_user(USERNAME, PASSWORD)
    token = login_user(USERNAME, PASSWORD)

    # Use session (cookies) for session-based context OR set header if using token
    session.headers.update({"Authorization": f"Bearer {token}"})

    create_session("My Test Session")
    send_text_chat("Hello from the test script!")
    send_multimodal_chat("What do you see in this image?", IMAGE_PATH)
    get_sessions()
    get_messages()

# 🤖 Hybrid AI Chatbot - LLM + Vision + Auth + Session

A production-ready AI chatbot with a modular Flask backend, modern frontend, user authentication, image understanding (CLIP/LLaVA-ready), persistent chat sessions, and Dockerized deployment.

---

## 📁 Project Structure

```
chatbot_production/
│
├── app.py                   # Main Flask entry point
├── .env                     # Environment variables
├── .gitignore               # Git ignore file
├── Dockerfile               # Docker build file
├── docker-compose.yml       # Docker Compose configuration
├── nginx.conf               # Nginx reverse proxy configuration
├── gunicorn_config.py       # Gunicorn production configuration
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
│
├── config/                  # Configuration modules
│
├── core/                    # Backend logic
│   ├── auth.py              # Authentication handlers
│   ├── llm.py               # LLM API interface
│   ├── vision.py            # Vision model handler
│   ├── session_handler.py   # Session management
│   ├── utils.py             # Shared utilities
│   └── __init__.py
│
├── data/
│   └── database.sqlite      # SQLite database
│
├── logs/                    # Logging directory
│
├── models/                  # AI model files
│   ├── llm_backend.py
│   └── vision_model.py
│
├── routes/                  # Flask route modules
│   ├── auth_routes.py
│   ├── chat_routes.py
│   └── session_routes.py
│
├── static/
│   ├── images/              # Static images
│   ├── scripts/             # Frontend scripts
│   │   ├── auth.js
│   │   ├── chat.js
│   │   ├── session.js
│   │   ├── upload.js
│   │   ├── utils.js
│   │   └── vision.js
│   └── styles/
│       └── style.css        # CSS styles
│
├── templates/
│   ├── index.html           # Chat UI
│   └── login.html           # Login UI
│
├── tests/                   # Test suite (to be implemented)
└── uploads/                 # Uploaded images
```

---

## ✅ Features

- LLM Chat (via API)
- Image Upload
- Session Tracking (SQLite)
- User Login/Logout (Flask session)
- Modular Frontend with JavaScript
- Dockerized Deployment (Gunicorn + Nginx)
- Environment Configuration (.env)

---

## 🚀 Getting Started

### 1. Install Requirements

```bash
pip install -r requirements.txt
```
---

### 2. Add `.env`

Create a `.env` file in the root directory:

```
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
```

---

### 3. Run Locally (Development)

```bash
python app.py
```

---

## 🐳 Docker Deployment

### Build and Start

```bash
docker-compose up --build
```

The app will be available at [http://localhost](http://localhost).

---

## 🧠 To-Do / Coming Soon

| Feature                             | Status |
|-------------------------------------|--------|
| Vision Inference (CLIP/LLaVA)       | ⏳ WIP |
| Image + Text Prompt Fusion          | ⏳ WIP |
| Session Export (Markdown/JSON)      | 🔜     |
| Usage Rate Limiting / API Tracking  | 🔜     |
| Admin Dashboard / Stats             | 🔜     |
| Switchable LLM Backend              | 🔜     |
| Automated Test Suite                | 🔜     |

---

## 📦 Tech Stack

| Component     | Tool                         |
|---------------|------------------------------|
| Backend       | Flask                        |
| Frontend      | HTML + CSS + Vanilla JS      |
| Auth          | Flask session (JWT planned)  |
| LLM API       | LLaMA / OpenAI               |
| Vision        | CLIP / LLaVA (future)        |
| Database      | SQLite                       |
| Deployment    | Docker, Gunicorn, Nginx      |

---

## 🤝 Contributions

This is a beginner-friendly project designed for learning and experimentation. Contributions for improvements, bug fixes, model integration, and UI enhancements are welcome.

---

## 📜 License

This project is licensed under the MIT License. Use freely with proper attribution.

---

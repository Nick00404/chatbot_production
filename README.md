# 🤖 Hybrid AI Chatbot - Multimodal LLM + Vision + Auth + Sessions

A production-ready AI chatbot supporting **text + image inputs**, **JWT authentication**, **session tracking**, and **Dockerized deployment**. Built on a **modular Flask architecture**, ready for both experimentation and production environments.

---

## ✅ Features

- 💬 **Text Chat**: LLM-powered responses via OpenAI / Hugging Face
- 🖼️ **Multimodal Support**: Image + text input processing (CLIP/LLaVA-ready)
- 🔐 **JWT Authentication**: Secure token-based login
- 🧠 **Session Management**: Persistent, user-specific conversation logs
- ⚙️ **Modular Codebase**: Separated logic for auth, LLM, vision, and routes
- 🧪 **Testing Suite**: Modular unit tests
- 🐳 **Dockerized**: Gunicorn + Nginx setup for production deployment
- 🖥️ **Frontend**: HTML + CSS + JS interface with image upload support

---

## 📁 Project Structure

```
chatbot_production/
├── app.py                   # Flask entry point
├── .env                     # Environment config
├── Dockerfile               # Backend Docker container
├── docker-compose.yml    	 # Add Redis service
├── nginx.conf               # Reverse proxy config
├── requirements.txt         # Python dependencies
│
├── config/                  # Config modules (e.g., gunicorn)
│
├── core/                    # Core logic
│   ├── auth.py              # User auth
│   ├── llm.py               # LLM handlers
│   ├── vision.py            # Vision models (CLIP/LLaVA)
│   ├── session_handler.py   # Session lifecycle
│   └── utils.py             # Helpers
│   ├── security.py       	 # Rate limiting
│   ├── middleware.py     	 # Quotas
│   └── plugins/          	 # Extensibility
│
├── routes/                  # API endpoints
│   ├── auth_routes.py
│   ├── chat_routes.py
│   ├──	session_routes.py
│   └── admin_routes.py		 # Metrics endpoints
│
├── static/                  # Frontend assets
│   ├── scripts/             # JS (auth, chat, vision, admin, etc.)
│   └── styles/              # CSS stylesheets
│
├── templates/               # HTML templates
│   ├── index.html
│   └── login.html
│
├── uploads/                 # Uploaded user images
├── logs/                    # App logs
├── models/                  # Model wrappers (LLM & Vision)
├── data/
│   ├── database.sqlite
│   └── init_db.py           # DB init script
└── tests/                   # Unit tests
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker + Docker Compose
- OpenAI or Hugging Face API Key

### Local Setup

```bash
git clone https://github.com/yourusername/chatbot_production.git
cd chatbot_production
pip install -r requirements.txt
python data/init_db.py
python app.py
```

### Create `.env`

```ini
SECRET_KEY=your_secret_key
OPENAI_API_KEY=sk-xxx       # Optional
HF_API_TOKEN=hf-xxx         # Optional
HUGGINGFACE_MODEL=google/flan-t5-large
PORT=5000
DEBUG=false
```

---

## 📡 API Documentation

### Auth
| Endpoint              | Method | Description         |
|-----------------------|--------|---------------------|
| `/api/auth/register`  | POST   | Register new user   |
| `/api/auth/login`     | POST   | JWT-based login     |

### Chat
| Endpoint               | Method | Description             |
|------------------------|--------|-------------------------|
| `/api/chat`            | POST   | Text-based interaction  |
| `/api/chat/multimodal` | POST   | Image + text inputs     |

### Session
| Endpoint                   | Method | Description              |
|----------------------------|--------|--------------------------|
| `/api/session/`            | POST   | Start new session        |
| `/api/session/sessions`    | GET    | Get user sessions        |
| `/api/session/<id>`        | DELETE | Delete session           |

**Headers:**

```
Authorization: Bearer <JWT_TOKEN>
```

---

## 🧪 Testing

```bash
python -m pytest tests/ -v --disable-warnings
```

Covers:
- ✅ Registration/login
- ✅ Chat & multimodal requests
- ✅ Session creation & deletion

---

## 🐳 Docker Deployment

```bash
docker-compose build
docker-compose up -d
```

Open your browser at: `http://localhost:8000`

---

## 🧠 To-Do / Coming Soon

| Feature                             | Status |
|-------------------------------------|--------|
| Vision Inference (CLIP/LLaVA)       | ⏳ WIP |
| Image + Text Prompt Fusion          | ⏳ WIP |
| Session Export (Markdown/JSON)      | 🔜     |
| API Rate Limiting                   | 🔜     |
| Admin Dashboard                     | 🔜     |
| LLM Backend Switching               | 🔜     |
| Full Test Coverage                  | 🔜     |

---

## 🛆 Tech Stack

| Layer         | Tools                     |
|---------------|----------------------------|
| Backend       | Flask                      |
| Frontend      | HTML, CSS, Vanilla JS      |
| Auth          | JWT (Flask-JWT-Extended)   |
| LLMs          | OpenAI, Hugging Face       |
| Vision Models | CLIP / LLaVA               |
| DB            | SQLite                     |
| Deployment    | Docker, Gunicorn, Nginx    |

---

## 🤝 Contributing

1. Fork the repo
2. Create a new branch:
```bash
git checkout -b feature/my-feature
```
3. Push and open a PR 🚀

---

## 📜 License

MIT License - See [LICENSE](LICENSE)

---


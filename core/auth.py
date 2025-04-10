# backend/auth.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env into environment

AUTHORIZED_API_KEY = os.getenv("API_KEY")

def is_authorized(token):
    return token == AUTHORIZED_API_KEY

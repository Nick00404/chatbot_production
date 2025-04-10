# backend/auth.py
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env into environment

AUTHORIZED_API_KEY = os.getenv("API_KEY")

def is_authorized(token):
    return token == AUTHORIZED_API_KEY

# core/auth.py

def verify_user(username, password):
    # check user from DB or dummy data
    return True  # or real logic

def hash_password(password):
    # return hashed password string
    return password  # or real hashing

def check_credentials(username, password):
    # Your logic here
    pass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
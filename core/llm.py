# backend/llm.py
import requests
import os

LLAMA_API_URL = os.getenv("LLAMA_API_URL") or "http://localhost:11434/api/generate"

def query_llm(prompt, session_id="default"):
    payload = {
        "model": "llama3",  
        "prompt": prompt,
        "stream": False,
        "session_id": session_id
    }
    try:
        response = requests.post(LLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "⚠️ No response from model.")
    except Exception as e:
        return f"❌ LLM Error: {e}"

def get_llm_response(prompt):
    # Your logic using LLaMA API
    pass
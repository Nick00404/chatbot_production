# backend/session_handler.py
import sqlite3
import os

DB_PATH = "data/sessions.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        message TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_message(session_id, role, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (session_id, role, message) VALUES (?, ?, ?)", (session_id, role, message))
    conn.commit()
    conn.close()

def get_session_messages(session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role, message FROM sessions WHERE session_id = ?", (session_id,))
    data = cursor.fetchall()
    conn.close()
    return [{"role": role, "message": msg} for role, msg in data]

def delete_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

# core/session_handler.py

import sqlite3


DB_PATH = "data/database.sqlite"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Makes rows behave like dictionaries
    return conn

# Create a new chat session for a user
def create_session(user_id, name="Untitled Session"):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions (user_id, name)
        VALUES (?, ?)
    """, (user_id, name))

    conn.commit()
    session_id = cursor.lastrowid
    conn.close()
    return session_id

# Delete a session and all associated messages
def delete_session(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    conn.commit()
    conn.close()

# List all sessions for a specific user
def get_sessions_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, created_at
        FROM sessions
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    sessions = cursor.fetchall()
    conn.close()
    return [dict(row) for row in sessions]

# Save a message in a session
def save_message(session_id, sender, message):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, sender, message)
        VALUES (?, ?, ?)
    """, (session_id, sender, message))

    conn.commit()
    conn.close()

# Get all messages for a specific session
def get_messages_for_session(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sender, message, timestamp
        FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
    """, (session_id,))

    messages = cursor.fetchall()
    conn.close()
    return [dict(row) for row in messages]

def get_all_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions ORDER BY created_at DESC')
    sessions = cursor.fetchall()
    conn.close()
    return sessions


# Alias for backward compatibility
save_message_to_session = save_message


def init_db():
    """Initialize the database with required tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            sender TEXT,
            content TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')

    conn.commit()
    conn.close()

def get_session_messages(session_id):
    """Retrieve all messages for a given session ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT sender, content, timestamp FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
    ''', (session_id,))
    
    messages = cursor.fetchall()
    conn.close()
    
    return [
        {
            "sender": row[0],
            "content": row[1],
            "timestamp": row[2]
        }
        for row in messages
    ]
# core/session_handler.py

import sqlite3
import os

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
def get_sessions_for_user(user_id: int) -> list[dict]:
    """
    Retrieve all chat sessions for a specific user, ordered by most recent first.
    
    Args:
        user_id: The ID of the user whose sessions to retrieve
        
    Returns:
        List of session dictionaries with keys: id, name, timestamp
        
    Raises:
        ValueError: If user_id is not a positive integer
    """
    # Validate input
    if not isinstance(user_id, int) or user_id < 1:
        raise ValueError("user_id must be a positive integer")
    
    sessions = []
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, strftime('%Y-%m-%d %H:%M:%S', timestamp) AS timestamp
                FROM sessions
                WHERE user_id = ?
                ORDER BY timestamp DESC
            """, (user_id,))
            
            sessions = [dict(row) for row in cursor.fetchall()]
            
    except sqlite3.Error as e:
        print(f"Database error in get_sessions_for_user: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in get_sessions_for_user: {str(e)}")
        raise
        
    return sessions

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
        SELECT sender, content, timestamp
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



# core/session_handler.py (FIXED)
def init_db(db_path: str = None):
    """Initialize the database with required tables"""
    db_path = db_path or "data/database.sqlite"  # Use default if not provided
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
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


import sqlite3

DB_PATH = "data/database.sqlite"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Create a new chat session
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

# Delete a session and its messages
def delete_session(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    conn.commit()
    conn.close()
    return True


# Save a message
def save_message(session_id, sender, content):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, sender, content)
        VALUES (?, ?, ?)
    """, (session_id, sender, content))

    conn.commit()
    conn.close()

# Retrieve all messages for a session
def get_session_messages(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sender, content, timestamp
        FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
    """, (session_id,))

    messages = cursor.fetchall()
    conn.close()

    return [dict(row) for row in messages]

# Get all sessions (admin/debug)
def get_all_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions ORDER BY timestamp DESC')
    sessions = cursor.fetchall()
    conn.close()
    return [dict(row) for row in sessions]

def get_active_session_for_user(user_id):
    """Get the most recent (active) session for a user, if one exists."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM sessions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    return row["id"] if row else None

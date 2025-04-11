import sqlite3
from core.session_handler import init_db, create_session, save_message, get_session_messages

def test_message_saving(test_db):
    """
    Test core database operations for chat messages:
    - Session creation
    - Message saving
    - Message retrieval
    """
    # Initialize database with test path (via test_db fixture)
    init_db(test_db)

    # -------------------------------------------------------------------------
    # Step 1: Create a test user directly in DB (bypass auth for unit testing)
    # -------------------------------------------------------------------------
    with sqlite3.connect(test_db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("testuser", "testpass")
        )
        user_id = cursor.lastrowid  # Get auto-generated user ID
        conn.commit()

    # -------------------------------------------------------------------------
    # Step 2: Create a new session for this user
    # -------------------------------------------------------------------------
    session_id = create_session(user_id, "Unit Test Session")

    # -------------------------------------------------------------------------
    # Step 3: Save test messages
    # -------------------------------------------------------------------------
    save_message(session_id, "user", "Hello bot!")
    save_message(session_id, "bot", "Hi human!")

    # -------------------------------------------------------------------------
    # Step 4: Retrieve and verify messages
    # -------------------------------------------------------------------------
    messages = get_session_messages(session_id)

    # Basic checks
    assert len(messages) == 2, "Should have 2 saved messages"
    
    # Verify first message (user)
    assert messages[0]["sender"] == "user"
    assert "Hello bot!" in messages[0]["content"]
    
    # Verify second message (bot)
    assert messages[1]["sender"] == "bot"
    assert "Hi human!" in messages[1]["content"]
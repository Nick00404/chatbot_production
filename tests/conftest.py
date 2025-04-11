# tests/conftest.py

from typing import Generator
from pathlib import Path
import pytest
from app import app as flask_app
from core.session_handler import init_db
import sqlite3
import os

# Fixture: Clean test database for every test
@pytest.fixture(scope='function')
def test_db(tmp_path):
    db_path = str(tmp_path / "test_db.sqlite")
    init_db(db_path)  # Now accepts the path parameter
    yield db_path

# Fixture: Flask test client
@pytest.fixture
def client(test_db):
    flask_app.config['TESTING'] = True
    flask_app.config['DATABASE'] = test_db  # Use temp DB
    
    with flask_app.test_client() as client:
        yield client

# Fixture: Mock LLM/Vision to avoid real API calls
@pytest.fixture
def mock_llm(monkeypatch):
    def mock_query(*args, **kwargs):
        return "Mock LLM Response"
    monkeypatch.setattr('core.llm.query_llm', mock_query)

@pytest.fixture
def mock_vision(monkeypatch):
    def mock_caption(*args, **kwargs):
        return "Mock Image Caption"
    monkeypatch.setattr('core.vision.generate_caption', mock_caption)

@pytest.fixture(autouse=True)
def clean_db(test_db):
    with sqlite3.connect(test_db) as conn:
        conn.execute("DELETE FROM messages")
        conn.execute("DELETE FROM sessions")
        conn.execute("DELETE FROM users")
        conn.execute("DELETE FROM sqlite_sequence")  # Reset auto-increment IDs
        conn.commit()



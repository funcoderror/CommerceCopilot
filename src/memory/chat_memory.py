
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "chat_history.db"


def initialize_database():
    """Create or update the chat history table."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check whether session_id already exists
    cursor.execute("PRAGMA table_info(chat_history)")
    columns = [column[1] for column in cursor.fetchall()]

    if "session_id" not in columns:
        cursor.execute(
            "ALTER TABLE chat_history ADD COLUMN session_id TEXT"
        )

        # Assign existing messages to a legacy session
        cursor.execute("""
            UPDATE chat_history
            SET session_id = 'legacy'
            WHERE session_id IS NULL
        """)

    conn.commit()
    conn.close()


def save_message(role, content, session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (session_id, role, content)
        VALUES (?, ?, ?)
    """, (session_id, role, content))

    conn.commit()
    conn.close()


def get_history(session_id, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content
        FROM chat_history
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))

    messages = cursor.fetchall()
    conn.close()

    messages.reverse()

    return [
        {"role": role, "content": content}
        for role, content in messages
    ]


if __name__ == "__main__":
    initialize_database()
    print("Chat memory database initialized successfully!")

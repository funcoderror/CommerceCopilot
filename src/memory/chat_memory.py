
import sqlite3

DB_PATH = "chat_history.db"


def initialize_database():
    """Create the chat history table if it doesn't exist."""

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

    conn.commit()
    conn.close()


def save_message(role, content):
    """Save a user or assistant message."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (role, content)
        VALUES (?, ?)
    """, (role, content))

    conn.commit()
    conn.close()


def get_history(limit=10):
    """Retrieve the most recent conversation messages."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content
        FROM chat_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

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

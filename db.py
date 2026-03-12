import sqlite3
from datetime import datetime

DB_PATH = "notes.db"


def init_db():
    """Initialize the database and run any pending migrations."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            canvas_data TEXT
        )
    """)
    cursor.execute("PRAGMA table_info(notes)")
    columns = {row[1] for row in cursor.fetchall()}
    if "updated_at" not in columns:
        cursor.execute("ALTER TABLE notes ADD COLUMN updated_at TIMESTAMP")
        cursor.execute("UPDATE notes SET updated_at = created_at WHERE updated_at IS NULL")
    conn.commit()
    conn.close()


def get_notes():
    """Return all notes ordered by most recently updated."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM notes ORDER BY updated_at DESC")
    notes = cursor.fetchall()
    conn.close()
    return notes


def get_note(note_id: int):
    """Return (name, canvas_data) for a single note."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, canvas_data FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()
    return note


def create_note(name: str) -> int:
    """Insert a new note and return its id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (name, canvas_data, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
        (name, ""),
    )
    note_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return note_id


def save_note(note_id: int, canvas_data: str):
    """Persist canvas data and bump updated_at for the given note."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notes SET canvas_data = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (canvas_data, note_id),
    )
    conn.commit()
    conn.close()


def rename_note(note_id: int, new_name: str):
    """Update the name of a note."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notes SET name = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (new_name, note_id),
    )
    conn.commit()
    conn.close()


def delete_note(note_id: int):
    """Permanently remove a note from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

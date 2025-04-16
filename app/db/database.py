import sqlite3
from datetime import datetime

DB_PATH = "app/db/photos.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_photo_to_db(filename: str):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO photos (filename, created_at) VALUES (?, ?)",
        (filename, created_at)
    )
    conn.commit()
    conn.close()

def get_filtered_photos(start_date: str = "", end_date: str = ""):
    conn = get_db_connection()
    if start_date and end_date:
        try:
            photos = conn.execute(
                """
                SELECT filename, created_at 
                FROM photos 
                WHERE created_at BETWEEN ? AND ? 
                ORDER BY created_at DESC
                """,
                (start_date, end_date)
            ).fetchall()
        except ValueError:
            photos = []
    else:
        photos = conn.execute(
            "SELECT filename, created_at FROM photos ORDER BY created_at DESC LIMIT 10"
        ).fetchall()

    conn.close()
    return photos

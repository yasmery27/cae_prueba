import sqlite3
from config import DATABASE_PATH


def get_connection():
    try:
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        return connection
    except sqlite3.Error as error:
        raise RuntimeError(f"Error conectando DB: {error}")


def initialize_database():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            location TEXT NOT NULL,
            budget TEXT NOT NULL,
            saved_at TEXT NOT NULL
        )
        """)

        connection.commit()

    except sqlite3.Error as error:
        raise RuntimeError(f"Error creando tablas: {error}")

    finally:
        connection.close()

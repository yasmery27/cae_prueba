import sqlite3
import pandas as pd
from config import DB_PATH

def get_connection():
    """Establece conexión resiliente. Errores: ConnectionError."""
    try:
        return sqlite3.connect(DB_PATH, check_same_thread=False)
    except sqlite3.Error as e:
        raise ConnectionError(f"Falla crítica en base de datos: {e}")

def initialize_db():
    """Crea y puebla la base de datos si no existe. Falla fuerte si no puede escribir."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lugares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT,
                zona TEXT,
                precio_avg INTEGER,
                mood TEXT,
                lat REAL,
                lon REAL
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM lugares")
        if cursor.fetchone()[0] == 0:
            lugares_seed = [
                ('Mamey Librería', 'Cultura/Café', 'Zona Colonial', 800, 'Calmado', 18.4727, -69.8856),
                ('Local 3', 'Brunch/Bar', 'Piantini', 1500, 'Vibrante', 18.4735, -69.9320),
                ('Parque Iberoamérica', 'Aire Libre', 'Gazcue', 200, 'Calmado', 18.4650, -69.9130),
                ('The Woods', 'Bar/Nightlife', 'Naco', 2500, 'Vibrante', 18.4750, -69.9250),
                ('Lulú Tasting Bar', 'Cena/Tragos', 'Zona Colonial', 2200, 'Vibrante', 18.4715, -69.8840),
                ('La Alpargatería', 'Cultura/Café', 'Zona Colonial', 950, 'Calmado', 18.4740, -69.8860)
            ]
            cursor.executemany('''
                INSERT INTO lugares (nombre, categoria, zona, precio_avg, mood, lat, lon)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', lugares_seed)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error fatal inicializando DB: {e}")
    finally:
        conn.close()

def get_all_places():
    """Lectura segura de datos para UI."""
    conn = get_connection()
    try:
        return pd.read_sql_query("SELECT * FROM lugares", conn)
    except Exception as e:
        raise RuntimeError(f"No se pudieron leer los datos: {e}")
    finally:
        conn.close()

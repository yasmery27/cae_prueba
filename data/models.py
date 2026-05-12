from datetime import datetime
import pandas as pd

from data.database import get_connection


def save_plan(event_name, location, budget):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO saved_plans (
                event_name,
                location,
                budget,
                saved_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                event_name,
                location,
                budget,
                datetime.utcnow().isoformat()
            )
        )

        connection.commit()
        return True

    except Exception as error:
        raise RuntimeError(f"Error guardando plan: {error}")

    finally:
        connection.close()


def fetch_saved_plans():
    connection = get_connection()

    try:
        query = "SELECT * FROM saved_plans ORDER BY id DESC"
        dataframe = pd.read_sql_query(query, connection)

        return dataframe

    except Exception as error:
        raise RuntimeError(f"Error leyendo planes: {error}")

    finally:
        connection.close()

import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="QueHacerSD",
    layout="wide"
)

# ---------- DATABASE ----------
conn = sqlite3.connect("events.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS saved_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT,
    location TEXT,
    budget TEXT,
    saved_at TEXT
)
""")
conn.commit()

# ---------- MOCK DATA ----------
events_data = [
    {
        "Evento": "Brunch Creativo",
        "Zona": "Zona Colonial",
        "Precio": "RD$800",
        "Ambiente": "Calmado",
        "Horario": "Diurno",
        "Descripcion": "Brunch con música suave y espacio para conversar."
    },
    {
        "Evento": "Jazz Nights",
        "Zona": "Piantini",
        "Precio": "RD$1500",
        "Ambiente": "Relajado",
        "Horario": "Nocturno",
        "Descripcion": "Música en vivo y ambiente tranquilo."
    },
    {
        "Evento": "Ruta del Chicharrón",
        "Zona": "Villa Mella",
        "Precio": "RD$500",
        "Ambiente": "Criollo",
        "Horario": "Diurno",
        "Descripcion": "Recorrido gastronómico local."
    },
# ---------- SIDEBAR ----------
st.sidebar.title("Filtros")

budget_filter = st.sidebar.selectbox(
    "Presupuesto",
    ["Todos", "RD$500", "RD$800", "RD$1500"]
)

zone_filter = st.sidebar.selectbox(
    "Zona",
    ["Todas", "Zona Colonial", "Piantini", "Villa Mella"]
)

schedule_filter = st.sidebar.selectbox(
    "Horario",
    ["Todos", "Diurno", "Nocturno"]
)

# ---------- TITLE ----------
st.title("QueHacerSD")
st.subheader("Descubre y organiza planes en Santo Domingo")

st.info(
    "Encuentra eventos con información clara de precio, ambiente y ubicación."
)

# ---------- FILTERING ----------
filtered_events = []
for event in events_data:
    matches_budget = budget_filter == "Todos" or event["Precio"] == budget_filter
    matches_zone = zone_filter == "Todas" or event["Zona"] == zone_filter
    matches_schedule = schedule_filter == "Todos" or event["Horario"] == schedule_filter

    if matches_budget and matches_zone and matches_schedule:
        filtered_events.append(event)
# ---------- EVENT CARDS ----------
for event in filtered_events:
    with st.container(border=True):
        st.markdown(f"## {event['Evento']}")
        st.write(event["Descripcion"])

        col1, col2, col3 = st.columns(3)

        col1.metric("Zona", event["Zona"])
        col2.metric("Precio", event["Precio"])
        col3.metric("Horario", event["Horario"])

        st.caption(f"Ambiente: {event['Ambiente']}")

        if st.button(f"Guardar plan · {event['Evento']}"):
            cursor.execute(
                """
                INSERT INTO saved_plans (event_name, location, budget, saved_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    event["Evento"],
                    event["Zona"],
                    event["Precio"],
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                )
            )
            conn.commit()
            st.success("Plan guardado")
# ---------- SAVED PLANS ----------
st.divider()

st.header("Planes guardados")

saved_df = pd.read_sql_query(
    "SELECT * FROM saved_plans ORDER BY id DESC",
    conn
)

if saved_df.empty:
    st.write("Todavía no has guardado planes.")
else:
    st.dataframe(saved_df, use_container_width=True)

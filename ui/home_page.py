import streamlit as st

from config import (
    APP_TITLE,
    APP_SUBTITLE,
    VALID_BUDGETS,
    VALID_ZONES,
    VALID_SCHEDULES,
    SUCCESS_MESSAGE
)

from data.mock_events import EVENTS
from data.models import save_plan, fetch_saved_plans

from logic.event_filters import filter_events
from logic.event_validators import validate_event

from external.logger import log_error


def render_home_page():
    st.title(APP_TITLE)
    st.subheader(APP_SUBTITLE)

    st.sidebar.title("Filtros")

    budget = st.sidebar.selectbox(
        "Presupuesto",
        VALID_BUDGETS
    )

    zone = st.sidebar.selectbox(
        "Zona",
        VALID_ZONES
    )

    schedule = st.sidebar.selectbox(
        "Horario",
        VALID_SCHEDULES
    )

    filtered_events = filter_events(
        EVENTS,
        budget,
        zone,
        schedule
    )

    for event in filtered_events:

        if not validate_event(event):
            st.error("Evento inválido.")
            continue

        with st.container(border=True):

            st.markdown(f"## {event['Evento']}")
            st.write(event["Descripcion"])

            col1, col2, col3 = st.columns(3)

            col1.metric("Zona", event["Zona"])
            col2.metric("Precio", event["Precio"])
            col3.metric("Horario", event["Horario"])

            st.caption(f"Ambiente: {event['Ambiente']}")

            button_label = f"Guardar · {event['Evento']}"

            if st.button(button_label):

                try:
                    save_plan(
                        event["Evento"],
                        event["Zona"],
                        event["Precio"]
                    )

                    st.success(SUCCESS_MESSAGE)

                except Exception as error:
                    st.error(log_error(str(error)))

    st.divider()

    st.header("Planes guardados")

    try:
        saved_plans = fetch_saved_plans()

        if saved_plans.empty:
            st.write("No hay planes guardados.")
        else:
            st.dataframe(
                saved_plans,
                use_container_width=True
            )

    except Exception as error:
        st.error(log_error(str(error)))

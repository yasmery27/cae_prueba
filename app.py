import streamlit as st
import sys
import os

# Asegurar que el path local se reconozca en Streamlit Cloud
sys.path.append(os.path.dirname(__file__))

from config.py import APP_NAME, DEFAULT_BUDGET, ZONES, MOODS
from data.database.py import initialize_db, get_all_places
from logic.filters.py import apply_search_filters
from logic.planner.py import calculate_total_cost, is_budget_exceeded
from ui.styles.py import inject_brand_css
from ui.components.py import render_map, place_card

# Inicialización con feedback de carga
if 'db_ready' not in st.session_state:
    with st.spinner("Certificando datos de la ciudad..."):
        initialize_db()
        st.session_state.db_ready = True

st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="📍")
inject_brand_css()

# Estado de sesión para itinerario
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = []

st.title(f"📍 {APP_NAME}")
st.caption("La fuente confiable para el ocio local en Santo Domingo.")

# Sidebar de control
with st.sidebar:
    st.header("Tu Perfil de Salida")
    budget = st.slider("¿Cuánto quieres gastar? (RD$)", 0, 5000, DEFAULT_BUDGET, help="Ajustamos las sugerencias a tu 'funda de cuarto'.")
    zones = st.multiselect("Zonas de interés", ZONES, default=ZONES)
    mood = st.radio("Ambiente", ["Todos"] + MOODS, horizontal=True)
    
    st.divider()
    if st.button("🔄 Reiniciar búsqueda", use_container_width=True):
        st.session_state.itinerary = []
        st.rerun()

# Carga de datos con manejo de error
try:
    df = get_all_places()
    filtered_df = apply_search_filters(df, budget, zones, mood)
except Exception as e:
    st.error(f"Error al conectar con la base de datos local: {e}")
    st.stop()

# Layout Principal
col_map, col_list = st.columns([2, 1])

with col_map:
    st.subheader("Mapa de Opciones")
    render_map(filtered_df)
    
with col_list:
    st.subheader("Lugares Sugeridos")
    if filtered_df.empty:
        st.info("No encontramos lugares con esos filtros. Prueba subiendo tu presupuesto o cambiando de zona.")
    else:
        def add_to_plan(item):
            st.session_state.itinerary.append(item.to_dict())
            st.toast(f"✅ {item['nombre']} añadido al plan", icon="🎉")

        for _, row in filtered_df.iterrows():
            place_card(row, add_to_plan)

# Sección de Itinerario con lógica de negocio
st.divider()
st.header("📋 Mi Planificación")

if not st.session_state.itinerary:
    st.visual_layout = st.empty()
    st.info("Tu itinerario está vacío. Explora el mapa y añade lugares para calcular tu salida.")
else:
    total = calculate_total_cost(st.session_state.itinerary)
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.metric("Total Estimado", f"RD${total}")
    with c2:
        if is_budget_exceeded(total, budget):
            st.warning(f"⚠️ Excediste tu presupuesto por RD${total - budget}")
        else:
            st.success("✅ Estás dentro del presupuesto.")
    with c3:
        if st.button("Limpiar plan completo", type="secondary"):
            st.session_state.itinerary = []
            st.rerun()

    # Mostrar lista compacta
    for item in st.session_state.itinerary:
        st.write(f"🔹 **{item['nombre']}** — {item['zona']} (RD${item['precio_avg']})")

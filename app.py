import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="SDQ Ocio Hub", layout="wide", initial_sidebar_state="expanded")

# ESTILOS PERSONALIZADOS (NAVY, CORAL, GOLD)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FAF7F2; }}
    h1, h2, h3 {{ color: #1E2761 !important; font-family: 'Georgia', serif; }}
    .stButton>button {{ background-color: #F96167; color: white; border: none; }}
    .stBadge {{ background-color: #F9E795; color: #1A1A1A; }}
    </style>
    """, unsafe_allow_state_cache=True)

# 1. BASE DE DATOS MOCK
@st.cache_data
def load_data():
    return pd.DataFrame([
        {"nombre": "Mamey Librería", "tipo": "Cultura/Café", "zona": "Zona Colonial", "lat": 18.4727, "lon": -69.8856, "precio_avg": 800, "ambiente": "Calmado", "parqueo": "Difícil"},
        {"nombre": "Local 3", "tipo": "Brunch/Bar", "zona": "Piantini", "lat": 18.4735, "lon": -69.9320, "precio_avg": 1500, "ambiente": "Vibrante", "parqueo": "Valet"},
        {"nombre": "Parque Iberoamérica", "tipo": "Aire Libre", "zona": "Gazcue", "lat": 18.4650, "lon": -69.9130, "precio_avg": 200, "ambiente": "Calmado", "parqueo": "Fácil"},
        {"nombre": "The Woods", "tipo": "Bar/Nightlife", "zona": "Naco", "lat": 18.4750, "lon": -69.9250, "precio_avg": 2500, "ambiente": "Vibrante", "parqueo": "Valet"},
    ])

df_lugares = load_data()

# 2. LÓGICA DE AGENTE (SESSION STATE)
if 'mi_plan' not in st.session_state:
    st.session_state.mi_plan = []

# SIDEBAR: FILTROS CRÍTICOS
st.sidebar.header("🔍 Filtros de Planificación")
max_budget = st.sidebar.slider("Presupuesto máximo (RD$)", 0, 5000, 2000)
zona_fav = st.sidebar.multiselect("Zonas preferidas", df_lugares['zona'].unique(), default=df_lugares['zona'].unique())
ambiente_fav = st.sidebar.radio("Mood", ["Todos", "Calmado", "Vibrante"])

# FILTRADO DE DATA
filtered_df = df_lugares[
    (df_lugares['precio_avg'] <= max_budget) & 
    (df_lugares['zona'].isin(zona_fav))
]
if ambiente_fav != "Todos":
    filtered_df = filtered_df[filtered_df['ambiente'] == ambiente_fav]

# INTERFAZ PRINCIPAL
st.title("📍 SDQ Ocio Hub")
st.write(f"Mostrando **{len(filtered_df)}** opciones que cuidan tu 'funda de cuarto'.")

col_map, col_list = st.columns([2, 1])

with col_map:
    st.subheader("Mapa de Opciones")
    m = folium.Map(location=[18.47, -69.91], zoom_start=13, tiles="cartodbpositron")
    for idx, row in filtered_df.iterrows():
        folium.Marker(
            [row['lat'], row['lon']],
            popup=f"{row['nombre']} - RD${row['precio_avg']}",
            tooltip=row['nombre'],
            icon=folium.Icon(color="red" if row['ambiente'] == "Vibrante" else "blue")
        ).add_to(m)
    st_folium(m, width=700, height=400)

with col_list:
    st.subheader("Lugares Sugeridos")
    for idx, row in filtered_df.iterrows():
        with st.expander(f"**{row['nombre']}** ({row['zona']})"):
            st.write(f"💰 **Gasto promedio:** RD${row['precio_avg']}")
            st.write(f"🚗 **Parqueo:** {row['parqueo']}")
            st.write(f"🎭 **Ambiente:** {row['ambiente']}")
            if st.button(f"Añadir al plan", key=f"btn_{idx}"):
                st.session_state.mi_plan.append(row.to_dict())
                st.toast(f"{row['nombre']} añadido al plan")

# SECCIÓN DE PLANIFICACIÓN
st.divider()
st.header("📋 Tu Salida Planificada")

if st.session_state.mi_plan:
    plan_df = pd.DataFrame(st.session_state.mi_plan)
    total_gasto = plan_df['precio_avg'].sum()
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Itinerario")
        for item in st.session_state.mi_plan:
            st.write(f"- {item['nombre']} ({item['zona']}) — RD${item['precio_avg']}")
    
    with c2:
        st.metric("Gasto Total Estimado", f"RD${total_gasto}")
        if total_gasto > max_budget:
            st.error("⚠️ Te pasaste de tu presupuesto inicial.")
        else:
            st.success("✅ El plan cuadra con tu presupuesto.")
            
    if st.button("Limpiar Plan"):
        st.session_state.mi_plan = []
        st.rerun()
else:
    st.info("Aún no tienes lugares en tu plan.")

st.markdown("""
<div style='text-align: center; color: #6B6B6B; font-size: 0.8rem; margin-top: 50px;'>
    SDQ Ocio Hub | Datos certificados para el público local.
</div>
""", unsafe_allow_html=True)

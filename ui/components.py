import streamlit as st
import folium
from streamlit_folium import st_folium
from config import COLOR_NAVY, COLOR_CORAL

def render_map(df):
    """Componente de mapa con estados de carga."""
    if df.empty:
        st.info("🗺️ El mapa está esperando filtros para mostrar opciones.")
        return

    # Crear mapa
    m = folium.Map(
        location=[18.475, -69.91], 
        zoom_start=13, 
        tiles="cartodbpositron"
    )

    for _, row in df.iterrows():
        color = 'red' if row['mood'] == 'Vibrante' else 'blue'
        folium.Marker(
            [row['lat'], row['lon']],
            popup=folium.Popup(f"<b>{row['nombre']}</b><br>RD${row['precio_avg']}", max_width=200),
            tooltip=row['nombre'],
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)

    st_folium(m, width="100%", height=450, key="main_map")

def place_card(row, on_add_callback):
    """Tarjeta visual con microcopy de producto."""
    with st.expander(f"📍 {row['nombre']}"):
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Zona:** {row['zona']}")
            st.write(f"**Gasto:** RD${row['precio_avg']}")
        with c2:
            st.write(f"**Ambiente:** {row['mood']}")
            st.write(f"**Tipo:** {row['categoria']}")
        
        st.button(
            f"Seleccionar lugar", 
            key=f"add_{row['id']}", 
            on_click=on_add_callback, 
            args=(row,)
        )

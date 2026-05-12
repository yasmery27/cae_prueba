import streamlit as st
from config import COLOR_NAVY, COLOR_CORAL, COLOR_GOLD, COLOR_CREAM

def inject_brand_css():
    """Inyecta el sistema de diseño para el demo."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Georgia&display=swap');
        
        .stApp {{ 
            background-color: {COLOR_CREAM}; 
        }}
        
        .main h1 {{ 
            font-family: 'Georgia', serif;
            color: {COLOR_NAVY};
            font-weight: 700;
        }}
        
        .stButton>button {{
            width: 100%;
            border-radius: 8px;
            border: 1px solid {COLOR_CORAL};
            background-color: white;
            color: {COLOR_CORAL};
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            background-color: {COLOR_CORAL};
            color: white;
        }}
        
        /* Estilo de tarjetas */
        .stExpander {{
            background-color: white !important;
            border: 1px solid #E0E0E0 !important;
            border-radius: 8px !important;
            margin-bottom: 10px !important;
        }}
        
        /* Metric values */
        [data-testid="stMetricValue"] {{
            color: {COLOR_NAVY};
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

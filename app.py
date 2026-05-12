import streamlit as st

from data.database import initialize_database
from ui._brand import inject_styles
from ui.home_page import render_home_page

st.set_page_config(
    page_title="QueHacerSD",
    layout="wide"
)

initialize_database()
inject_styles()

render_home_page()

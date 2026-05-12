import streamlit as st


def inject_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FAF7F2;
        }

        h1, h2, h3 {
            color: #1E2761;
        }

        div.stButton > button {
            background-color: #F96167;
            color: white;
            border-radius: 8px;
            border: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

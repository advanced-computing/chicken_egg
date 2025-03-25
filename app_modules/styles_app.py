import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
            body, .stApp { background-color: black; color: white; }
            h1, h2, h3, h4, h5, h6, p, div { color: white !important; }

            header { background-color: black !important; }

            .block-container {
                padding-top: 50px !important;
            }

            .stSidebar {
                background-color: #333333 !important;
            }
            .stSidebar div, .stSidebar p, .stSidebar span {
                color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
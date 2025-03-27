import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
            /* App background and text */
            body, .stApp {
                background-color: black;
                color: white;
            }

            /* General text styling */
            h1, h2, h3, h4, h5, h6, p, div, span {
                color: white !important;
            }

            /* Top header */
            header {
                background-color: black !important;
            }

            /* Main content container */
            .block-container {
                padding-top: 50px !important;
                background-color: black !important;
                color: white !important;
            }

            /* Sidebar styling */
            .stSidebar {
                background-color: #222222 !important;
            }
            .stSidebar div, .stSidebar p, .stSidebar span {
                color: white !important;
            }

            /* Buttons */
            .stButton > button {
                color: white;
                background-color: #444444;
                border: none;
            }

            /* Text inputs, text areas, select boxes, number inputs */
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox div,
            .stMultiSelect div,
            .stNumberInput input {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
            }

            /* DataFrames and tables */
            .stDataFrame, .stTable {
                background-color: #1e1e1e !important;
                color: white !important;
            }

            /* Plotly background fix */
            .stPlotlyChart {
                background-color: #1e1e1e !important;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

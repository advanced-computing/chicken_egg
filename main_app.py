# main_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from app_modules.styles_app import apply_styles
from app_modules.tabs_app import (
    render_tab1_project_proposal,
    render_tab2_bird_flu,
    render_tab3_egg_stocks
)

def render_combined_dashboard():
    st.subheader("📊 Combined Dashboard")
    
    # Example CPI and Egg Prices Data
    cpi_data = pd.DataFrame({
        "Month": pd.date_range(start="2020-01-01", periods=12, freq="M"),
        "CPI": [250, 252, 255, 258, 260, 262, 265, 268, 270, 273, 275, 278],
        "Egg Prices": [1.5, 1.6, 1.7, 1.8, 2.0, 2.1, 2.3, 2.5, 2.6, 2.8, 3.0, 3.2]
    })

    # Create Scatter Plot
    fig = px.scatter(
        cpi_data,
        x="CPI",
        y="Egg Prices",
        title="CPI vs Egg Prices",
        labels={"CPI": "Consumer Price Index", "Egg Prices": "Egg Prices ($)"},
        template="plotly_white"
    )
    st.plotly_chart(fig)

def main():
    apply_styles()
    st.title("🐔 Chicken Economics: Unpacking Bird Flu, Egg Prices & Market Signals")
    st.markdown("### Contributors")
    st.write("Arnav Sahai")
    st.write("Fred Lee")
    st.write("Angel Ragas")

    # Sidebar for Tabs
    st.sidebar.markdown("<h2 style='font-size:20px;'>Navigation</h2>", unsafe_allow_html=True)
    tab = st.sidebar.radio(
        "Select a Tab:",
        ["📘 Project Proposal", "🦠 Bird Flu Data", "🥚 Egg Prices & Stocks", "📊 Combined Dashboard"]
    )

    # Render Tabs
    if tab == "📘 Project Proposal":
        render_tab1_project_proposal()
    elif tab == "🦠 Bird Flu Data":
        render_tab2_bird_flu()
    elif tab == "🥚 Egg Prices & Stocks":
        render_tab3_egg_stocks()
    elif tab == "📊 Combined Dashboard":
        render_combined_dashboard()

if __name__ == "__main__":
    main()
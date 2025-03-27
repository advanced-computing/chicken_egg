# main_app.py

import streamlit as st
from app_modules.styles_app import apply_styles
from app_modules.tabs_app import (
    render_tab1_project_proposal,
    render_tab2_bird_flu,
    render_tab3_egg_stocks,
    render_tab4_dashboard
)

def main():
    apply_styles()
    st.title("🐔 Chicken Economics: Unpacking Bird Flu, Egg Prices & Market Signals")
    st.markdown("### Contributors")
    st.write("Arnav Sahai")
    st.write("Fred Lee")
    st.write("Angel Ragas")

    # Define tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📘 Project Proposal",
        "🦠 Bird Flu Data",
        "🥚 Egg Prices & Stocks",
        "📊 Combined Dashboard"
    ])

    with tab1:
        render_tab1_project_proposal()

    with tab2:
        render_tab2_bird_flu()

    with tab3:
        render_tab3_egg_stocks()

    with tab4:
        render_tab4_dashboard()

if __name__ == "__main__":
    main()

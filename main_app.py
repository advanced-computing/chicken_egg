# main_app.py

import streamlit as st
st.set_page_config(page_title="Chicken Economics", layout="wide")  # ✅ MUST BE FIRST

from app_modules.styles_app import apply_styles
from app_modules.tabs_app import (
    render_tab1_about_app,
    render_tab2_bird_flu,
    render_tab3_egg_stocks,
    render_tab4_dashboard,
    render_tab5_appendix
)

def main():
    apply_styles()

    # Sidebar tab selection (vertical layout)
    tab = st.sidebar.radio("🗂️ Select a section", [
        "📘 About the App",
        "🦠 Bird Flu Data",
        "🥚 Egg Prices & Stocks",
        "📊 Combined Dashboard",
        "📚 Appendix"
    ])

    st.title("🐔 Chicken Economics: Unpacking Bird Flu, Egg Prices & Market Signals")
    st.markdown("### Contributors")
    st.write("Fred Lee")
    st.write("Arnav Sahai")
    st.write("Angel Ragas")

    # Tab logic
    if tab == "📘 About the App":
        render_tab1_about_app()
    elif tab == "🦠 Bird Flu Data":
        render_tab2_bird_flu()
    elif tab == "🥚 Egg Prices & Stocks":
        render_tab3_egg_stocks()
    elif tab == "📊 Combined Dashboard":
        render_tab4_dashboard()
    elif tab == "📚 Appendix":
        render_tab5_appendix()

if __name__ == "__main__":
    main()

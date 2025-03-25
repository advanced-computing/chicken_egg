# app_modules/tabs_app.py

import streamlit as st
from app_modules.visualizations_app import (
    show_price_comparison,
    show_bird_flu_trends,
    show_combined_dashboard,
    show_wild_bird_map
)
from app_modules.functions_app import (
    prep_bird_flu_data,
    prep_egg_price_data,
    prep_stock_price_data,
    prep_wild_bird_data
)

# === TAB 1 ===
def render_tab1_project_proposal():
    st.image("https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_modules/rooster.jpg", caption="What came first, the chicken or the egg?", use_container_width=True)

    st.header("Project Proposal")
    st.markdown("# Overview")
    st.markdown("""
    This project explores the relationship between bird flu outbreaks, egg price fluctuations, and the financial performance of key egg producers. 
    Our analysis aims to address several research questions, including:
    """)
    st.markdown("""
    1. **What is the relationship between the increase of bird flu outbreaks and increases in Grade A egg prices? Is there a time lag?**
    2. **How does the stock price of Cal-Maine Foods (the largest egg company in the USA) respond to bird flu outbreaks?**
    3. **What areas are at risk based on the integration of wild bird and commercial flock data?**
    4. **How are non-caged egg producers such as Vital Farms affected by egg prices and bird flu outbreaks?**
    5. **How is the largest processor of value-added eggs, Michael Foods, affected by egg prices and bird flu outbreaks?**
    """)

# === TAB 2 ===
def render_tab2_bird_flu():
    wild_bird_geo = prep_wild_bird_data(
        wild_bird_data='https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/prep_data/wild_birds.csv',
        fips='https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/prep_data/state_and_county_fips_master.csv',
        geolocators='https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/prep_data/cfips_location.csv'
    )
    bird_data = prep_bird_flu_data('https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/prep_data/bird_flu.csv')

    total_chicken_deaths = bird_data['Flock Size'].sum()
    total_wild_bird_infections = len(wild_bird_geo)
    latest_date_str = wild_bird_geo['Date Detected'].max()

    col1, col2, col3 = st.columns(3)
    col1.metric("Cumulative Chicken Deaths", f"{total_chicken_deaths:,}")
    col2.metric("Total Wild Bird Infections", f"{total_wild_bird_infections:,}")
    col3.metric("Latest Wild Bird Detection", latest_date_str)

    st.subheader("Commercial Bird Flu Outbreaks")
    show_bird_flu_trends()

    st.subheader("Wild Bird Infections Map")
    show_wild_bird_map(wild_bird_geo, bird_data)

# === TAB 3 ===
def render_tab3_egg_stocks():
    egg_data = prep_egg_price_data('https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/egg_price_monthly.csv')

    stock_option = st.selectbox(
        'Select Stock to Compare Against Egg Prices',
        options=['Cal-Maine', 'Post Holdings', 'Vital Farms']
    )

    st.markdown("""
    - **Cal-Maine** Largest egg producer in the US accounting for 20% of production  
    - **Post Holdings** Owns Michael Foods, a value-added egg product producer  
    - **Vital Farms** Pasture-raised eggs, leading specialty brand  
    """)

    stock_file_map = {
        "Cal-Maine": "app_data/calmaine_prices_daily.csv",
        "Post Holdings": "app_data/post_prices_daily.csv",
        "Vital Farms": "app_data/vitl_prices_daily.csv"
    }

    selected_stock_data = prep_stock_price_data(stock_file_map[stock_option])
    show_price_comparison(egg_data, selected_stock_data, stock_name=stock_option)

# === TAB 4 ===
def render_tab4_dashboard():
    show_combined_dashboard()

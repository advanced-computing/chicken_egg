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
    st.image("app_modules/rooster.jpg", caption="What came first, the chicken or the egg?", use_container_width=True)

    st.header("🔍 Revisiting the Proposal: Insights & Adjustments")
    
    st.markdown("## **Reflections on Chicken & Egg App Improvements**")
    st.markdown("---")
    
    st.markdown("### 🗓️ **Team Review Milestone**")
    st.markdown("""
    On **March 26, 2025**, the team finalized the architecture of the Chicken & Egg app.  
    Key modules and data pipelines were reviewed to ensure performance, scalability, and clarity.
    """)

    st.markdown("## 📌 **Key Adjustments & Solutions**")

    st.markdown("### 🔹 **1. Centralized Data Structure**")
    st.markdown("""
    - **Issue:** Files were scattered and difficult to track.  
    - ✅ **Solution:** Structured folders:  
        - 📂 `app_data` for raw & prepared datasets  
        - ⚙️ `app_modules` for visualization & data prep functions  
        - ☁️ `app_bigquery` for upload logic  
    """)

    st.markdown("### 🔹 **2. GitHub Data Integration**")
    st.markdown("""
    - **Issue:** Files were originally read only from local sources.  
    - ✅ **Solution:** Updated paths to fetch data dynamically from GitHub or BigQuery when needed.
    """)

    st.markdown("### 🔹 **3. BigQuery Uploader Modules**")
    st.markdown("""
    - **Issue:** No cloud sync for preprocessed data.  
    - ✅ **Solution:** Created `app_bigquery/` with:
        - `upload_bird_flu.py`
        - `upload_wild_birds.py`
        - `upload_egg_prices.py`
        - `upload_stock_prices.py`
    """)

    st.markdown("### 🔹 **4. New Data Prep Functions**")
    st.markdown("""
    - **Issue:** Legacy functions didn't support remote/cloud-based files.  
    - ✅ **Solution:** Refactored `functions_app.py` to support flexible loading and tested outputs.
    """)

    st.markdown("### 🔹 **5. Modularization & Testing**")
    st.markdown("""
    - **Issue:** Testing and debugging was hard due to tight coupling of scripts.  
    - ✅ **Solution:** Introduced:
        - `app_tests/` for test scripts
        - `app_modules/helper_modules/geodata.py` for geolocation logic
    """)

    st.markdown("### 🔹 **6. GeoJSON & Visualization Enhancements**")
    st.markdown("""
    - **Issue:** Mapping wild bird outbreaks lacked spatial context.  
    - ✅ **Solution:** Integrated `us_states.geojson` and cleaned spatial joins.
    """)

    st.markdown("## 🛠️ **Technical Milestones**")

    st.markdown("""
    - 🧹 Data cleaned & uploaded to BigQuery  
    - 📦 Modules refactored into reusable pipelines  
    - 🧪 Unit tests in place for core logic  
    - ☁️ Data now syncs between GitHub and BigQuery for scalable access
    """)

    st.markdown("## 📌 **Final Takeaways & Next Steps**")

    st.markdown("""
    1️⃣ **Cloud-first design**: BigQuery as single source of truth  
    2️⃣ **Scalable architecture**: Code is modular, testable, and production-ready  
    3️⃣ **Next:** Automate incremental uploads and expand visual dashboards with Streamlit  
    """)

    st.success("🚀 All changes have been integrated into the current app version.")

# === TAB 2 ===
def render_tab2_bird_flu():
    wild_grouped, valid_states = prep_wild_bird_data("wild_birds")
    bird_data = prep_bird_flu_data("bird_flu", group_by_state = True)

    total_chicken_deaths = bird_data['Flock Size'].sum()
    total_wild_bird_infections = wild_grouped['Wild Count'].sum()
    latest_date_str = wild_grouped.sort_values('Month')['Month_str'].iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("Cumulative Chicken Deaths", f"{total_chicken_deaths:,}")
    col2.metric("Total Wild Bird Infections", f"{total_wild_bird_infections:,}")
    col3.metric("Latest Wild Bird Detection", latest_date_str)

    st.subheader("Commercial Bird Flu Outbreaks")
    show_bird_flu_trends()

    st.subheader("Wild Bird Infections Map")
    show_wild_bird_map(wild_grouped, bird_data, valid_states)

# === TAB 3 ===
def render_tab3_egg_stocks():
    
    stock_option = st.selectbox(
        'Select Stock to Compare Against Egg Prices',
        options=['Cal-Maine', 'Post Holdings', 'Vital Farms']
    )

    st.markdown("""
    - **Cal-Maine** Largest egg producer in the US accounting for 20% of production  
    - **Post Holdings** Owns Michael Foods, a value-added egg product producer  
    - **Vital Farms** Pasture-raised eggs, leading specialty brand  
    """)

    stock_table_map = {
        "Cal-Maine": "calmaine",
        "Post Holdings": "post",
        "Vital Farms": "vitl"
    }

    # Big Query data load
    egg_data = prep_egg_price_data('egg_prices')
    
    calmaine_df, vitl_df, post_df = prep_stock_price_data()
    stock_dfs = {
        "calmaine": calmaine_df,
        "vitl": vitl_df,
        "post": post_df
    }
    selected_stock_df = stock_dfs[stock_table_map[stock_option]]   


    show_price_comparison(egg_data, selected_stock_df, stock_name=stock_option)

# === TAB 4 ===
def render_tab4_dashboard():
    show_combined_dashboard()

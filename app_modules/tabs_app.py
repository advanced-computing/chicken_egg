import streamlit as st
from app_modules.visualizations_app import (
    show_price_comparison,
    show_bird_flu_trends,
    show_combined_dashboard,
    show_wild_bird_map,
    show_flock_county_choropleth,
)
from app_modules.functions_app import (
    prep_bird_flu_data,
    prep_egg_price_data,
    prep_stock_price_data,
    prep_wild_bird_data
)

# === TAB 1 ===
def render_tab1_about_app():
    st.image("app_modules/rooster.jpg", caption="What came first, the chicken or the egg?", use_container_width=True)

    st.title("📊 Chicken Economics: Understanding Egg Prices & Avian Flu")
    st.markdown("---")

    st.markdown("### 🧠 What Is This Dashboard?")
    st.markdown("""
    **Chicken Economics** is an interactive data dashboard designed to explore how egg prices, avian flu outbreaks, and stock market signals interact over time.

    Built with **Streamlit** and powered by **Google BigQuery**, it allows users to analyze diverse datasets through simple, intuitive visualizations.
    """)

    st.markdown("#### 🧾 Historical Note")
    st.info("This app evolved from a project proposal reviewed on March 26, 2025, where the modular structure, data pipelines, and visualization goals were defined.")

    st.markdown("### 🔍 Research Questions")
    st.markdown("""
    - How have avian flu outbreaks influenced the trajectory of egg prices in the U.S.?  
    - Can upstream indicators (like wild bird flu detections) help anticipate price volatility?  
    - How did egg-producing companies (e.g., Cal-Maine) respond to market shifts?
    """)

    st.markdown("### 📊 Data Sources")
    st.markdown("""
    | Dataset                 | Description                                |
    |-------------------------|--------------------------------------------|
    | **Egg Prices**          | Monthly retail data (CSV → BigQuery)       |
    | **Wild Bird Surveillance** | Flu presence in birds (scraped data)     |
    | **Stock Prices**        | Equity performance (e.g., Cal-Maine Foods) |
    """)

    st.markdown("### ⚙️ Methodology")
    st.markdown("""
    1. **Data Collection**: Raw data is scraped or uploaded from CSVs.  
    2. **Data Upload**: Files are processed and pushed to BigQuery using scripts from `app_bigquery/`.  
    3. **Data Access**: Streamlit connects to BigQuery via SQL queries.  
    4. **Visualization**: Tabs display results using `Plotly`, `pandas`, and Streamlit widgets.  
    """)

    st.markdown("### 🧱 Modular Architecture")
    st.markdown("""
    - `main_app.py`: Streamlit entry point  
    - `app_modules/`: Logic for tabs, visuals, styles  
    - `app_bigquery/`: Loaders to BigQuery  
    - `app_data/`: Scraping tools  
    - `app_tests/`: Data validation scripts  
    - `airflow_home/`: DAGs (future automation)
    """)

    st.markdown("### 📂 What You’ll Find in This App")
    st.markdown("""
    - 🦠 **Bird Flu**: Visualize outbreaks across U.S. states by species and time  
    - 🥚 **Egg & Stock Prices**: Compare egg pricing trends with stock performance  
    - 📊 **Combined Dashboard**: Explore all datasets together to detect correlations  
    - 📚 **Appendix**: Deep technical documentation, sources, and variable dictionaries
    """)

    st.markdown("### 🚀 Ready to Explore")
    st.success("Navigate through the tabs to explore flu trends, price changes, stock behavior, and more.")


# === TAB 2 ===
def render_tab2_bird_flu():
    wild_grouped, valid_states = prep_wild_bird_data("wild_birds")
    
    bird_data_state = prep_bird_flu_data("bird_flu", group_by = 'state')
    
    bird_data_county = prep_bird_flu_data("bird_flu", group_by="county")

    total_chicken_deaths = bird_data_state['Flock Size'].sum()
    total_wild_bird_infections = wild_grouped['Wild Count'].sum()
    latest_date_str = wild_grouped.sort_values('Month')['Month_str'].iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("Cumulative Chicken Deaths", f"{total_chicken_deaths:,}")
    col2.metric("Total Wild Bird Infections", f"{total_wild_bird_infections:,}")
    col3.metric("Latest Wild Bird Detection", latest_date_str)

    st.subheader("Commercial Bird Flu Outbreaks")
    show_bird_flu_trends()

    st.subheader("Wild Bird Infections Map")
    show_wild_bird_map(wild_grouped, bird_data_state, valid_states)
    
    st.subheader("Bird Flu County Level Data")
    show_flock_county_choropleth(bird_data_county)

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

    st.markdown("---")
    st.header("Key Insights from Combined Data")

    st.subheader("1. Avian Flu Outbreaks Coincide with Stock Price Spikes")
    st.markdown("""
    During major bird flu outbreaks—especially in 2022 and early 2023—**Cal-Maine's stock price surged** while overall flock populations plummeted.  
    This suggests that market expectations around egg shortages or reduced supply **benefit industry leaders financially**, despite the biological crisis.
    """)

    st.subheader("2. Egg Prices React to Supply Shocks, but with Lag")
    st.markdown("""
    Egg prices increased sharply following large-scale flock deaths, but **not always immediately**.  
    This indicates that **market pricing mechanisms adjust with a lag**, possibly due to production contracts or delayed retail reactions.
    """)

    st.subheader("3. Vital Farms Stock Less Sensitive to Flu Shocks")
    st.markdown("""
    Compared to Cal-Maine or Post Holdings, **Vital Farms stock showed less volatility** during avian flu peaks.  
    This supports the idea that **specialty or pasture-raised brands are less exposed** to large-scale outbreaks in commercial flocks.
    """)

    st.subheader("4. Correlations Suggest Speculative Market Behavior")
    st.markdown("""
    Some of the stock movements appear **disproportionate to real production losses**, hinting at speculation.  
    Investors may respond to **news cycles rather than just fundamentals**, a key insight for market risk analysis.
    """)

    st.subheader("5. Volatility Is Concentrated Around Seasonal Transitions")
    st.markdown("""
    Sharp movements in prices and stock returns tend to cluster around **late winter and early spring**,  
    likely linked to seasonal demand changes, policy updates, or flu transmission cycles.  
    Future forecasting models should factor in **time-of-year effects**.
    """)

# === TAB 5 ===
def render_tab5_appendix():
    st.title("📚 Appendix")
    st.markdown("""
    This appendix provides a comprehensive technical overview of the Chicken Economics dashboard.
    It includes metadata, sources, processing logic, schemas, storage architecture, and design notes.
    All information has been curated based on the actual project implementation.
    """)
    st.markdown("---")

    st.header("📊 Data Sources Overview")

    st.subheader("🥚 Egg Prices (USA)")
    st.markdown("""
    - **Origin**: U.S. Department of Agriculture (USDA) / public commodity datasets  
    - **Content**: Monthly time series of egg prices in the United States  
    - **Granularity**: National-level (no regional segmentation as of now)  
    - **Acquisition**: Downloaded and prepared manually as CSV  
    - **Storage Location**: BigQuery — table: `egg_prices_us`  
    - **Update Method**: Manual uploads using `app_bigquery/upload_egg_prices.py`  
    - **Key Fields**:
        - `date` (YYYY-MM)  
        - `price_usd` (float)  
        - `category` (e.g., retail, wholesale)
    - **Preprocessing**:
        - Checked for missing months and price outliers  
        - Converted price strings to float and standardized dates  
        - Harmonized column names for consistency
    """)

    st.subheader("🦠 Wild Bird Flu Surveillance")
    st.markdown("""
    - **Source**: Scraped CSVs from publicly available avian flu tracking sources  
    - **Acquisition Method**: Semi-automated download via `app_data/download_csv.py`  
    - **Content**: Confirmed detections of avian influenza in wild birds  
    - **Geographic Scope**: U.S. states, linked via state codes  
    - **Storage Location**: BigQuery — table: `wild_bird_flu_us`  
    - **Update Method**: `app_bigquery/upload_wild_birds.py`  
    - **Geo Enhancement**: Merged with `us_states.geojson` for state-level mapping  
    - **Key Fields**:
        - `date`, `state`, `species`, `flu_cases`, `source_file`
    - **Notes**:
        - Filtered to exclude non-wild bird reports  
        - Preprocessed for null species and malformed entries  
        - Combined reports by date-state-species triplet
    """)

    st.subheader("📈 Stock Prices (Cal-Maine Foods)")
    st.markdown("""
    - **Source**: Yahoo Finance — daily close prices  
    - **Focus Company**: Cal-Maine Foods (Ticker: CALM)  
    - **Frequency**: Daily  
    - **Acquisition**: CSV-based input  
    - **Storage Location**: BigQuery — table: `stock_prices_us`  
    - **Update Method**: `app_bigquery/upload_stock_prices.py`  
    - **Key Fields**:
        - `date`, `ticker`, `open`, `close`, `high`, `low`, `volume`
    - **Preprocessing**:
        - Verified date continuity  
        - Converted string columns to numeric  
        - Standardized schema for compatibility with other time series
    """)

    st.markdown("---")
    st.header("📄 Variable Dictionary")

    st.subheader("Egg Prices Table")
    st.markdown("""
    | Variable     | Type    | Description                          |
    |--------------|---------|--------------------------------------|
    | `date`       | string  | Month of observation (`YYYY-MM`)     |
    | `price_usd`  | float   | Price in U.S. dollars                |
    | `category`   | string  | Type of price (e.g., retail/wholesale)
    """)

    st.subheader("Wild Bird Flu Table")
    st.markdown("""
    | Variable     | Type    | Description                              |
    |--------------|---------|------------------------------------------|
    | `date`       | string  | Date of detection                        |
    | `state`      | string  | U.S. state abbreviation (e.g., NY, CA)   |
    | `species`    | string  | Bird species where flu was detected      |
    | `flu_cases`  | int     | Number of flu detections (if known)      |
    | `source_file`| string  | Original filename or report ID           |
    """)

    st.subheader("Stock Prices Table")
    st.markdown("""
    | Variable     | Type    | Description                          |
    |--------------|---------|--------------------------------------|
    | `date`       | string  | Trading date                        |
    | `ticker`     | string  | Stock ticker (e.g., CALM)           |
    | `open`       | float   | Opening price                       |
    | `close`      | float   | Closing price                       |
    | `high`       | float   | Daily high                          |
    | `low`        | float   | Daily low                           |
    | `volume`     | int     | Volume of shares traded             |
    """)

    st.markdown("---")
    st.header("⚙️ Technical Architecture & Design")

    st.markdown("""
    - **Framework**: Built with [Streamlit](https://streamlit.io) for interactive UI  
    - **Backend**: Google BigQuery for data storage and fast querying  
    - **Secrets Management**: `.streamlit/secrets.toml` includes:
        - `project_id`: GCP project name  
        - `credentials_path`: Full path to the JSON service account
    - **Query Layer**: Python functions in `query_gbq.py` use `pandas_gbq` and caching  
    - **Geo Mapping**: Flu surveillance data enriched via spatial joins with `us_states.geojson`  
    - **Folder Organization**:
        - `app_modules/`: Layout logic, visuals, and shared components  
        - `app_bigquery/`: Upload pipelines (CSV → BigQuery)  
        - `app_data/`: Scrapers and raw file downloaders  
        - `app_tests/`: Basic unit test structure for modularity  
        - `airflow_home/`: Optional future DAGs for automation
    - **Scalability**: Easily extendable to add new data sources or dashboards
    """)

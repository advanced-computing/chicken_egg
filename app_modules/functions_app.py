import pandas as pd
from .helper_modules.geodata import add_state_abbreviations, merge_with_fips, merge_with_geolocation, has_geospatial_columns, ensure_geospatial
from .query_gbq import query_table
from google.api_core.exceptions import GoogleAPIError
import streamlit as st

REQUIRED_GEO_COLS = ["fips", "lat", "lng"]


# This filepath will be used later for the National Ag. Stats Service API
#file_path = "https://quickstats.nass.usda.gov/results/AE779404-2B32-375F-B3FE-F48335DE30EC"

@st.cache_data(ttl=3600)
def prep_wild_bird_data(table_name="wild_birds"):
    """
    Cleans wild bird data and adds geospatial data.
    Returns a df with a 'lat' and 'lng' column for mapping.
    """
    # Load the wild bird data
    wild_bird_data = query_table(
        table_name,
        columns = ["State", "County", "Date Detected", "Bird Species"])
    
    # Formatting columns (GET RID OF THIS)
    wild_bird_data['State'] = wild_bird_data['State'].str.title()
    
    # Daily column = 'Date'
    wild_bird_data['Date'] = pd.to_datetime(
        wild_bird_data['Date Detected'], errors='coerce'
        ).dt.to_period("M").dt.to_timestamp()

    # Monthly column = 'Month'
    wild_bird_data['Month'] = wild_bird_data['Date'].dt.to_period("M").dt.to_timestamp()

    # Ensure that required columns exist
    required_columns = {"State", "County"}
    missing_columns = required_columns - set(wild_bird_data.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    wild_bird_geo = ensure_geospatial(wild_bird_data, source_name="wild_birds")


    # Validate that the resulting DataFrame contains 'lat' and 'lng'
    if "lat" not in wild_bird_geo.columns.tolist() or "lng" not in wild_bird_geo.columns.tolist():
        raise KeyError("Missing required columns: 'lat' and 'lng'")   
    
    wild_grouped = wild_bird_geo.groupby(['Month', 'State']).size().reset_index(name='Wild Count')
    wild_grouped['Month_str'] = wild_grouped['Month'].dt.strftime("%b %Y")

    # Extract valid states for filtering geojson
    valid_states = wild_grouped['State'].unique().tolist() 



    return wild_grouped, valid_states


@st.cache_data(ttl=3600)
def prep_bird_flu_data(table_name="bird_flu",
                       bird_flu_data=None, 
                       use_bigquery=True,
                       group_by="state"): 
    '''
    Loads and cleans bird flu data
    group_by_state=True indicates function will be used for map
    Returns either monthly aggregated data or geospatially grouped data by state. 
    '''

    selected_cols = ["Outbreak Date", "Flock Size"]
    if group_by == "state":
        selected_cols += ["State", "lat", "lng"]
    if group_by == "county":
        selected_cols += ["State", "County", "fips", "lat", "lng"]

    bird_flu_raw = None
    if use_bigquery:
        try:
            bird_flu_raw = query_table(table_name, columns=selected_cols)
            if bird_flu_raw is not None:
                    bird_flu_raw = bird_flu_raw.copy()        
                    print("Loaded bird flu data from BigQuery.")
        except GoogleAPIError as e:
            print(f"BigQuery failed: {e}")
        except Exception as e:
            print(f"Unknown error pulling from BigQuery: {e}")
    

    # Read the bird flu data from the provided file or DataFrame
    if bird_flu_raw is None:
        if isinstance(bird_flu_data, str):
            bird_flu_raw = pd.read_csv(bird_flu_data, usecols=selected_cols)
        elif isinstance(bird_flu_data, pd.DataFrame):
            bird_flu_raw = bird_flu_data[selected_cols].copy()
        else:
            raise ValueError("No data source")

    # Column validation
    missing_columns = set(selected_cols) - set(bird_flu_raw.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")
    
    bird_flu_raw["Date"] = pd.to_datetime(bird_flu_raw["Outbreak Date"], errors="coerce")

    # Exit early if not including geospatial data
    if group_by == "none":
            return bird_flu_raw.groupby("Date")["Flock Size"].sum().reset_index()

    bird_flu_raw["Month"] = bird_flu_raw["Date"].dt.to_period("M").dt.to_timestamp()
    bird_flu_raw["Month_str"] = bird_flu_raw["Month"].dt.strftime("%b %Y")
    if "State" in bird_flu_raw.columns:
        bird_flu_raw["State"] = bird_flu_raw["State"].str.title()
    if "County" in bird_flu_raw.columns:  
        bird_flu_raw["County"] = bird_flu_raw["County"].str.title()

    
    # skipping geospatial if cols already present
    if "County" in bird_flu_raw.columns:
        bird_flu_geo = ensure_geospatial(bird_flu_raw, source_name="bird_flu")
    else:
        print("Skipping ensure_geospatial — no 'County' column in data")
        bird_flu_geo = bird_flu_raw.copy()


    if "lat" not in bird_flu_geo.columns or "lng" not in bird_flu_geo.columns:
        raise KeyError("Missing required columns: 'lat' and 'lng'")
    
    # Ensure lat/lng are numeric for aggregation
    bird_flu_geo["lat"] = pd.to_numeric(bird_flu_geo["lat"], errors="coerce")
    bird_flu_geo["lng"] = pd.to_numeric(bird_flu_geo["lng"], errors="coerce")

    
    if group_by == "state":
        group_fields = ["Month", "State"]
    elif group_by == "county":
        group_fields = ["Month", "State", "County", "fips"]
    else:
        raise ValueError("group_by must be either 'state' or 'county'")

    grouped_bird_flu = bird_flu_geo.groupby(group_fields).agg({
        "Flock Size": "sum",
        "lat": "mean",
        "lng": "mean"
    }).reset_index()
    

    month_str_map = bird_flu_raw[["Month", "Month_str"]].drop_duplicates()
    grouped_bird_flu = grouped_bird_flu.merge(month_str_map, on="Month", how="left")
    
    return grouped_bird_flu

@st.cache_data(ttl=3600)
def prep_egg_price_data(
    egg_price_data='https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/egg_price_monthly.csv',
    use_bigquery=True,
    table_name="egg_prices"
    ):
    """
    Loads preformatted egg price data (monthly), parses 'Date' column,
    and returns a DataFrame ready for time series visualization.
    """
    
    df = None
    if use_bigquery:
        try:
            df = query_table(table_name, columns = ["Date", "Avg_Price"])
            print("Loaded egg price data from BigQuery.")
        except GoogleAPIError as e:
            print(f" BigQuery failed: {e}")
            raise
    
    if df is None:
        df = pd.read_csv(egg_price_data)

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y')

    # Set 'Date' as index and sort
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    return df

@st.cache_data(ttl=3600)
def prep_stock_price_data(
    use_bigquery=True,
    table_names=["calmaine", "vitl", "post"]):
    '''
    Loads and cleans stock data
    returns df that can be used for time-sereis viz
    Note: data is daily
    Please use 'Close_Last' for timeseries
    '''


    processed_dfs = {}
    
    for name in table_names:
        try:
            df = query_table(name, columns = ["Date", "Close_Last"])
            print(f"Loaded stock price data for '{name}' from BigQuery.")
        except GoogleAPIError as e:
            print(f"BigQuery failed for '{name}': {e}")
            raise  

        # Validate that 'Close_Last' exists
        required_columns = {'Close_Last'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise KeyError(f"Table '{name}' is missing required columns: {missing_columns}")

        # formatting dates
        df['Date'] = pd.to_datetime(df['Date'], format = '%m/%d/%Y')
        df.sort_values('Date', inplace=True)
        
        # resampling prior to loading
        df = df.set_index("Date").resample("M").mean(numeric_only=True).reset_index()        
        
        processed_dfs[name] = df
    
    return processed_dfs["calmaine"], processed_dfs["vitl"], processed_dfs["post"]


if __name__ == "__main__":
    import pandas as pd

    # Test bird flu data
    bird_df = prep_bird_flu_data(table_name="bird_flu")
    print("📊 bird_df columns:", bird_df.columns)

    # Test wild bird data
    wild_df, _ = prep_wild_bird_data(table_name="wild_birds")
    print("🦅 wild_df columns:", wild_df.columns)

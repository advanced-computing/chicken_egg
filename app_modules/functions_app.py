import pandas as pd
from helper_modules.geodata import add_state_abbreviations, merge_with_fips, merge_with_geolocation
from query_gbq import query_table
from google.api_core.exceptions import GoogleAPIError


# This filepath will be used later for the National Ag. Stats Service API
#file_path = "https://quickstats.nass.usda.gov/results/AE779404-2B32-375F-B3FE-F48335DE30EC"

def prep_wild_bird_data():
    """
    Cleans wild bird data and adds geospatial data.
    Returns a df with a 'lat' and 'lng' column for mapping.
    """
    # Load the wild bird data
    wild_bird_data = query_table("bird_flu")

    # Ensure that required columns exist
    required_columns = {"State", "County"}
    missing_columns = required_columns - set(wild_bird_data.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    wild_bird_state_abbrev = add_state_abbreviations(wild_bird_data)
    wild_bird_with_fips = merge_with_fips(wild_bird_state_abbrev)
    wild_bird_geo = merge_with_geolocation(wild_bird_with_fips)    

    # Validate that the resulting DataFrame contains 'lat' and 'lng'
    if "lat" not in wild_bird_geo.columns.tolist() or "lng" not in wild_bird_geo.columns.tolist():
        raise KeyError("Missing required columns: 'lat' and 'lng'")

    return wild_bird_geo



def prep_bird_flu_data(
    bird_flu_data='https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/prep_data/bird_flu.csv',
    use_bigquery=True
):
    '''
    Loads and cleans bird flu data
    Returns df with geospatial indicators derived from fips
    'Flock size' shows how many birds have died
    lng and lat can be used to place on map
    Need to add API!! 
    '''
    
    bird_flu_raw = None
    if use_bigquery:
        try:
            bird_flu_raw = query_table("bird_flu")  # Table name must match BigQuery
            print("✅ Loaded bird flu data from BigQuery.")
        except GoogleAPIError as e:
            print(f"⚠️ BigQuery failed: {e}")
        except Exception as e:
            print(f"⚠️ Unknown error pulling from BigQuery: {e}")

    # Read the bird flu data from the provided file or DataFrame
    if isinstance(bird_flu_data, str) or bird_flu_data is None:
        bird_flu_raw = pd.read_csv(bird_flu_data)
    else:
        bird_flu_raw = bird_flu_data

    required_columns = {"State", "County", "Flock Size"}
    missing_columns = required_columns - set(bird_flu_raw.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

        # If input already has 'lat' and 'lng', assume it’s pre-merged; add State Abbrev if needed, then return.
    if "lat" in bird_flu_raw.columns and "lng" in bird_flu_raw.columns:
        print("DEBUG: Input DataFrame already has 'lat' and 'lng'. Skipping merge steps.")
        return bird_flu_raw
    
    bird_flu_state_abbrev = add_state_abbreviations(bird_flu_raw)
    bird_flu_with_fips = merge_with_fips(bird_flu_state_abbrev)
    bird_flu_geo = merge_with_geolocation(bird_flu_with_fips)

    # Final validation before returning
    if "lat" not in bird_flu_geo.columns.tolist() or "lng" not in bird_flu_geo.columns.tolist():
        raise KeyError("Missing required columns: 'lat' and 'lng'")

    # Final version of df
    return bird_flu_geo

def prep_egg_price_data(egg_price_data='https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/egg_price_monthly.csv'):
    """
    Loads preformatted egg price data (monthly), parses 'Date' column,
    and returns a DataFrame ready for time series visualization.
    """
    if egg_price_data is None:
        try:
            df = query_table("egg_prices")
            print("✅ Loaded egg price data from BigQuery.")
        except GoogleAPIError as e:
            print(f"⚠️ BigQuery failed: {e}")
            raise
    else:
        df = pd.read_csv(egg_price_data)

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y')

    # Set 'Date' as index and sort
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    return df

def prep_stock_price_data(stock_price_data = None):
    '''
    Loads and cleans stock data
    returns df that can be used for time-sereis viz
    Note: data is daily
    Please use 'Close/Last' for timeseries
    '''

    stock_table_names = ["calmaine", "vitl", "post"]
    processed_dfs = {}
    
    for name in stock_table_names:
        try:
            df = query_table(name)
            print(f"✅ Loaded stock price data for '{name}' from BigQuery.")
        except GoogleAPIError as e:
            print(f"⚠️ BigQuery failed for '{name}': {e}")
            raise  

    # Validate that 'Close/Last' exists
        required_columns = {'Close/Last'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise KeyError(f"Table '{name}' is missing required columns: {missing_columns}")

    
        df['Date'] = pd.to_datetime(df['Date'], format = '%m/%d/%Y')

    # Loops over each col to remove $ in stock prices
        for col in df.columns:
            if df[col].dtype == object and "$" in str(df[col].iloc[0]):
                    df[col] = df[col].str.replace('$', '', regex=False)
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    
    # Date set to index to resample
        df.sort_values('Date', inplace=True)
        processed_dfs[name] = df
    
    return processed_dfs["calmaine"], processed_dfs["vitl"], processed_dfs["post"]

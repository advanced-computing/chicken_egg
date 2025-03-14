import pandas as pd


# This filepath will be used later for the National Ag. Stats Service API
#file_path = "https://quickstats.nass.usda.gov/results/AE779404-2B32-375F-B3FE-F48335DE30EC"

def prep_wild_bird_data(wild_bird_data = 'wild_birds.csv',
                          fips = 'state_and_county_fips_master.csv',
                          geolocators = 'cfips_location.csv'):
    """
    Cleans wild bird data and adds geospatial data.
    Returns a df with a 'lat' and 'lng' column for mapping.
    """
    # Load the wild bird data
    wild_bird_data = pd.read_csv(wild_bird_data)

    # Ensure that required columns exist
    required_columns = {"State", "County"}
    missing_columns = required_columns - set(wild_bird_data.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    # Map state names to their abbreviations
    state_to_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
        "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
        "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
        "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC",
    }
    wild_bird_data['State Abbrev'] = wild_bird_data['State'].map(state_to_abbrev)

    # Load FIPS data for county matching
    fips_data = pd.read_csv(fips)
    # Clean county names by removing "County", "Borough", or "Parish"
    fips_data['name'] = fips_data['name'].str.replace(r' County| Borough| Parish', '', regex=True).str.strip()
    fips_data['fips'] = fips_data['fips'].astype(str)

    # Merge wild bird data with FIPS codes using County and State Abbrev
    wild_bird_fips = pd.merge(
        wild_bird_data,
        fips_data,
        left_on=['County', 'State Abbrev'],
        right_on=['name', 'state'],
        how='left'
    ).drop(columns=['name', 'state'])

    # Load geolocation data
    geodata = pd.read_csv(geolocators)
    geodata['cfips'] = geodata['cfips'].astype(str)

    # Merge to add latitude and longitude using the FIPS code
    wild_bird_geo = pd.merge(
        wild_bird_fips,
        geodata,
        left_on='fips',
        right_on='cfips',
        how='left'
    ).drop(columns=['cfips', 'name'])

    # Validate that the resulting DataFrame contains 'lat' and 'lng'
    if "lat" not in wild_bird_geo.columns.tolist() or "lng" not in wild_bird_geo.columns.tolist():
        raise KeyError("Missing required columns: 'lat' and 'lng'")

    return wild_bird_geo



def prep_bird_flu_data(bird_flu_data = 'bird_flu.csv',
                          fips = 'state_and_county_fips_master.csv',
                          geolocators = 'cfips_location.csv'):
    '''
    Loads and cleans bird flu data
    Returns df with geospatial indicators derived from fips
    'Flock size' shows how many birds have died
    lng and lat can be used to place on map
    Need to add API!! 
    '''

    # Read the bird flu data from the provided file or DataFrame
    if isinstance(bird_flu_data, str) or bird_flu_data is None:
        bird_flu_raw = pd.read_csv(bird_flu_data)
    else:
        bird_flu_raw = bird_flu_data  # Here

    required_columns = {"State", "County", "Flock Size"}
    missing_columns = required_columns - set(bird_flu_raw.columns)
    
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

        # If input already has 'lat' and 'lng', assume it’s pre-merged; add State Abbrev if needed, then return.
    if "lat" in bird_flu_raw.columns and "lng" in bird_flu_raw.columns:
        print("DEBUG: Input DataFrame already has 'lat' and 'lng'. Skipping merge steps.")
        return bird_flu_raw  # Return early if 'lat' and 'lng' are present.

    #Dictionary for matching values, drop DC?
    state_to_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", 
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
        "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
        "Rhode Island": "RI","South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
        "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC",
    }

    # Adding new column with abbreviations, which will be used for geospatial data (FIPS)
    bird_flu_raw['State Abbrev'] = bird_flu_raw['State'].map(state_to_abbrev)

    # FIPS assigns unique codes to counties/states in the USA
    fips_data = pd.read_csv('state_and_county_fips_master.csv')

    # Removing data values which cause mismatch. Not removing capitalization because it matches between the two
    fips_data['name'] = fips_data['name'].str.replace(r' County| Borough| Parish', '', regex=True).str.strip()
    fips_data['fips'] = fips_data['fips'].astype(str)

    # adding fips; fips needed for geospatial data later
    bird_flu_merged = pd.merge(bird_flu_raw, fips_data,
            left_on= ['County', 'State Abbrev'],
            right_on= ['name', 'state'],
            how = 'left'
            )

    # Dropping duplicate columns
    bird_flu_merged = bird_flu_merged.drop(columns=['name', 'state'])

    geodata = pd.read_csv('cfips_location.csv')
    geodata['cfips'] = geodata['cfips'].astype(str)

    # adding lat/lgng columns
    bird_flu_geo = pd.merge(bird_flu_merged, geodata,
                        left_on= 'fips',
                        right_on= 'cfips',
                        how = 'left'
                        )

    # Final validation before returning
    if "lat" not in bird_flu_geo.columns.tolist() or "lng" not in bird_flu_geo.columns.tolist():
        raise KeyError("Missing required columns: 'lat' and 'lng'")

    # Final version of df
    bird_flu_final = bird_flu_geo.drop(columns =['cfips', 'name'])
    return bird_flu_final


def prep_egg_price_data(egg_price_data = None):
    '''
    Loads egg data, converts to long format and formats date
    returns df that can be used for time-series viz
    Note: data is monthly
    Note 2: could drop Month and Year columns
    '''
    # Load from file only if no DataFrame is provided (for testing purposes)
    if egg_price_data is None:
        egg_price_data = pd.read_csv('egg_prices.csv', skiprows=9)

    # Here: Validate that 'Year' exists in the data
    if "Year" not in egg_price_data.columns:
        raise ValueError("Missing required column: 'Year'")


    # going from wide data to long
    egg_price_long = egg_price_data.melt(id_vars=['Year'], var_name='Month', value_name='Avg_Price')

    # year converted to concat; day will always be 01
    # Note: converting to MM/DD/YYYY for consistency 
    #       w/ stock_prices maybe not needed
    egg_price_long['Date'] = pd.to_datetime(
        egg_price_long['Year'].astype(str) + '-' +
        egg_price_long['Month'] +
        '-01',
        format = '%Y-%b-%d'
    ).dt.strftime('%m-%d-%Y')
    
    #converting to datetime & setting as index to work w/ shared axis
    egg_price_long["Date"] = pd.to_datetime(egg_price_long["Date"], format="%m-%d-%Y")

    
    # Sort by date index
    egg_price_long.set_index('Date', inplace=True)
    egg_price_long.sort_index(inplace=True)


    return egg_price_long

def prep_stock_price_data(stock_price_data = None):
    '''
    Loads and cleans stock data
    returns df that can be used for time-sereis viz
    Note: data is daily
    Please use 'Close/Last' for timeseries
    '''
    
    if stock_price_data is None:
        stock_prices = pd.read_csv('cal_main_stock.csv')
    elif isinstance(stock_price_data, str):
        stock_prices = pd.read_csv(stock_price_data)
    else:
        stock_prices = stock_price_data

    # Validate that 'Close/Last' exists
    required_columns = {'Close/Last'}
    missing_columns = required_columns - set(stock_prices.columns)
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    
    stock_prices['Date'] = pd.to_datetime(stock_prices['Date'], format = '%m/%d/%Y')

    # Loops over each col to remove $ in stock prices
    for col in stock_prices.columns:
        if stock_prices[col].dtype == object:
            if "$" in stock_prices[col].iloc[0]:
                stock_prices[col] = stock_prices[col].str.replace('$', '', regex=False)
                stock_prices[col] = pd.to_numeric(stock_prices[col])
                    
    # Date set to index to resample
    stock_prices.set_index('Date', inplace=True)

    
    return stock_prices
import pandas as pd
import numpy as np



# This filepath will be used later for the National Ag. Stats Service API
#file_path = "https://quickstats.nass.usda.gov/results/AE779404-2B32-375F-B3FE-F48335DE30EC"


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

    bird_flu_raw = pd.read_csv('bird_flu.csv')

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

    # Final version of df
    bird_flu_final = bird_flu_geo.drop(columns =['cfips', 'name'])
    
    return bird_flu_final


def prep_egg_price_data(egg_price_data = 'egg_prices.csv'):
    '''
    Loads egg data, converts to long format and formats date
    returns df that can be used for time-series viz
    Note: data is monthly
    Note 2: could drop Month and Year columns
    '''
    
    egg_price_raw = pd.read_csv('egg_prices.csv', skiprows= 9)

    # going from wide data to long
    egg_price_long = egg_price_raw.melt(id_vars=['Year'], var_name='Month', value_name='Avg_Price')

    # year converted to concat; day will always be 01
    # Note: converting to MM/DD/YYYY for consistency 
    #       w/ stock_prices maybe not needed
    egg_price_long['Date'] = pd.to_datetime(
        egg_price_long['Year'].astype(str) + '-' +
        egg_price_long['Month'] +
        '-01',
        format = '%Y-%b-%d'
    ).dt.strftime('%m-%d-%Y')

    return egg_price_long

def prep_stock_price_data(stock_price_data = 'cal_main_stock.csv'):
    '''
    Loads and cleans stock data
    returns df that can be used for time-sereis viz
    Note: data is daily
    Please use 'Close/Last' for timeseries
    '''
    stock_prices = pd.read_csv('cal_main_stock.csv')
    stock_prices['Date'] = pd.to_datetime(stock_prices['Date'], format = '%m/%d/%Y')

    # Date set to index to resample
    stock_prices.set_index('Date', inplace=True)

    # Taking average of weekly prices (is there another way that makes more sense?)
    stock_prices_weekly = stock_prices.resample('W').mean().reset_index()
    
    return stock_prices_weekly
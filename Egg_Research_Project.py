import pandas as pd
import numpy as np
import geopandas as gpd
import streamlit as st


# This filepath will be used later for the National Ag. Stats Service API
#file_path = "https://quickstats.nass.usda.gov/results/AE779404-2B32-375F-B3FE-F48335DE30EC"


'''
Following cells divide loading in the data
1) Bird Flu Geospatial Data (key variables: 'Flock Size', 'lng', 'lat')
2) Grade A Egg Prices
3) Cal-Main Foods Stock Prices 
'''
#%%
bird_flu_raw = pd.read_csv('bird_flu.csv')

# Optional Validation
# print(bird_flu_raw.describe())

#Changing datatypes; could likely refactor this
# print(bird_flu_raw.dtypes)
# bird_flu_raw['Outbreak Date'] = pd.to_datetime(bird_flu_raw['Outbreak Date'])
# print(bird_flu_raw.dtypes)

#Adding abbreviated state values to bird_flu_raw

#Dictionary for matching values, recommended to collapse. Could get rid of territories
state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}

# Adding new column with abbreviations, which will be used for geospatial data (FIPS)
bird_flu_raw['State Abbrev'] = bird_flu_raw['State'].map(state_to_abbrev)
print(bird_flu_raw.head(10))

# FIPS assigns unique codes to counties/states in the USA
fips_data = pd.read_csv('state_and_county_fips_master.csv')

# Removing data values which cause mismatch. Not removing capitalization because it matches between the two
fips_data['name'] = fips_data['name'].str.replace(r' County| Borough| Parish', '', regex=True).str.strip()
fips_data['fips'] = fips_data['fips'].astype(str)

print(bird_flu_raw.columns)

bird_flu_merged = pd.merge(bird_flu_raw, fips_data,
         left_on= ['County', 'State Abbrev'],
         right_on= ['name', 'state'],
         how = 'left'
         )
print(bird_flu_merged)

# Rename this to improve clarity on the variables name
bird_flu_clean = bird_flu_merged.drop(columns=['name', 'state'])

print(bird_flu_clean)

geodata = pd.read_csv('cfips_location.csv')

print(geodata)
geodata['cfips'] = geodata['cfips'].astype(str)
print(geodata.dtypes)

bird_flu = pd.merge(bird_flu_clean, geodata,
                    left_on= 'fips',
                    right_on= 'cfips',
                    how = 'left'
                    )

#print(bird_flu)

# Creating final version of df, ready to be used in geospatial representation
# Flock size shows how many birds have died
# lng and lat can be used to place on map
bird_flu = bird_flu.drop(columns =['cfips', 'name'])
print(bird_flu.columns)
print(bird_flu)

#%%

egg_price_raw = pd.read_csv('egg_prices.csv', skiprows= 9)

print(egg_price_raw)
print(egg_price_raw.columns)

# going from wide data to long
egg_price_long = egg_price_raw.melt(id_vars=['Year'], var_name='Month', value_name='Avg_Price')
print(egg_price_long)
print(egg_price_long.dtypes)

# converting year to string
egg_price_long['Year'] = egg_price_long['Year'].astype(str)
print(egg_price_long.dtypes)
print(egg_price_long.head(10))

# adding date column
egg_price_long['Date'] = pd.to_datetime(
    egg_price_long['Year'] + '-' +
    egg_price_long['Month'] +
    '-01',
    format = '%Y-%b-%d'
)

# Reformatting date to MM-DD-YYYY
egg_price_long["Date"] = egg_price_long["Date"].dt.strftime("%m-%d-%Y")

# Retaining Year and Month columns, but could drop.
print(egg_price_long.head(10))

# Optional Save
#egg_price_long.to_csv("egg_price_long.csv", index=False)


# %%

stock_prices = pd.read_csv('cal_main_stock.csv')

# optional inspection
# print(stock_prices.head(10))
# print(stock_prices.dtypes)

stock_prices['Date'] = pd.to_datetime(stock_prices['Date'], format = '%m/%d/%Y')

# optional validation
# print(stock_prices.head(10))
# print(stock_prices.dtypes)

'''
Please use 'Close/Last' and 'Date' columns for timeseries!
'''
print(stock_prices.columns)

# Optional Save
#stock_prices.to_csv('stock_prices.csv', index=False)
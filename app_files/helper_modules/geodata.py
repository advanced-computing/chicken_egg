import pandas as pd

# Step 1: Add state abbreviations
def add_state_abbreviations(df):
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
    df["State Abbrev"] = df["State"].map(state_to_abbrev)
    return df

# Step 2: Clean county names and merge with FIPS
def merge_with_fips(df, fips_path = 'https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/prep_data/state_and_county_fips_master.csv'):
    fips_data = pd.read_csv(fips_path)
    fips_data["name"] = fips_data["name"].str.replace(r" County| Borough| Parish", "", regex=True).str.strip()
    fips_data["fips"] = fips_data["fips"].astype(str)

    df_merged = pd.merge(
        df,
        fips_data,
        left_on=["County", "State Abbrev"],
        right_on=["name", "state"],
        how="left"
    )
    return df_merged.drop(columns=["name", "state"])

# Step 3: Merge latitude/longitude based on FIPS
def merge_with_geolocation(df, geolocator_path = 'https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/prep_data/cfips_location.csv'):
    geodata = pd.read_csv(geolocator_path)
    geodata["cfips"] = geodata["cfips"].astype(str)
    df_geo = pd.merge(df, geodata, left_on="fips", right_on="cfips", how="left")
    return df_geo.drop(columns=["cfips", "name"])
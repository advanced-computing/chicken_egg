from app_data.web_scraping.download_csv import download_csv
from app_modules.helper_modules.geodata import (
    add_state_abbreviations,
    merge_with_fips,
    merge_with_geolocation
)

import pandas as pd

def clean_bird_flu_data():
    csv_url = "https://www.cdc.gov/bird-flu/modules/situation-summary/commercial-backyard-flocks.csv"
    df = pd.read_csv(csv_url)
    print("🔹 Raw data loaded:")
    print(df.head())

    # Step 1: Standardize column names
    df.columns = df.columns.str.strip()
    df["State"] = df["State"].str.title()
    df["County"] = df["County"].str.title()
    df["Outbreak Date"] = pd.to_datetime(df["Outbreak Date"], errors="coerce")
 

    # Step 2: Add FIPS and geospatial data
    df = add_state_abbreviations(df)
    df = merge_with_fips(df)
    df = merge_with_geolocation(df)


    return df

# Optional for standalone testing
if __name__ == "__main__":
    final_df = clean_bird_flu_data()
    print("Final cleaned DataFrame:")
    print(final_df.head())

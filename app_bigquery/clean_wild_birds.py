import os
import pandas as pd

def clean_wild_birds(
    input_csv: str,
    output_csv: str
):
 
    # 1) Load
    df = pd.read_csv(input_csv)

    # 2) Drop columns we don't need
    to_drop = [
        "Submitting Agency",
        "Sampling Method",
        "HPAI Strain",
        "WOAH Classification",
        "Collection Date"
    ]
    df.drop(columns=[c for c in to_drop if c in df.columns], errors="ignore", inplace=True)

    # 3) Parse 'Date Detected'
    if "Date Detected" in df.columns:
        df["Date Detected"] = pd.to_datetime(df["Date Detected"], errors="coerce")

    # 4) Ensure target folder exists
    folder = os.path.dirname(output_csv)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    # 5) Save cleaned CSV
    df.to_csv(output_csv, index=False)
    print(f"Saved cleaned data to '{output_csv}'")

# Example usage:
if __name__ == "__main__":
    clean_wild_birds(
        input_csv="wild_birds_raw.csv",
        output_csv="app_data/prep_data/wild_birds.csv"
    )
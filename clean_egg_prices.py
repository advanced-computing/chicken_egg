import pandas as pd

def clean_egg_price_data():
    url = (
    "https://fred.stlouisfed.org/graph/fredgraph.csv"
    "?id=APU0000708111"
    "&cosd=2022-01-01"
)
    df = pd.read_csv(url)

    # Strip whitespace, rename columns
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df.rename(columns={"APU0000708111": "Avg_Price", "observation_date": "Date"}, inplace=True)

    # Parse dates and filter
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df[df["Date"] >= "2022-01-01"]

    # Set index, sort, and save
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    df.to_csv("cleaned_egg_prices.csv")

    print("✅ Cleaned data saved as 'cleaned_egg_prices.csv'")
    print(df.head())


if __name__ == "__main__":
    clean_egg_price_data()
import os
import pandas as pd
import requests
from datetime import datetime



def fetch_stock_data(symbol: str, save_as: str):
    '''
    This requrires the correct symbols to work. They are CALM, VITL, and POST (Could work for other stocks)
    save_as is the name of the file name and type you want
    '''
    today = datetime.today().strftime('%Y-%m-%d')
    url = (
        f"https://api.nasdaq.com/api/quote/{symbol}/historical"
        f"?assetclass=stocks&fromdate=2015-01-01&todate={today}"
        f"&limit=9999"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Referer": f"https://www.nasdaq.com/market-activity/stocks/{symbol.lower()}/historical"
    }

    print(f"Downloading full historical data for {symbol}")
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    json_data = response.json()
    rows = json_data["data"]["tradesTable"]["rows"]

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    # Rename columns to match CSV structure
    df.rename(columns={
        "date": "Date",
        "close": "Close_Last",
        "volume": "Volume",
        "open": "Open",
        "high": "High",
        "low": "Low"
    }, inplace=True)

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Clean numeric columns
    for col in ["Close_Last", "Open", "High", "Low", "Volume"]:
        df[col] = (
            df[col]
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

    df.sort_values("Date", inplace=True)
    
    out_dir = "app_data"
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, save_as)
    
    df.to_csv(out_path, index=False)
    print(f"{symbol} data saved to {out_path}")

# Example
if __name__ == "__main__":
    fetch_stock_data("CALM", "calmaine_stock.csv")
    fetch_stock_data("VITL", "vitl_stock.csv")
    fetch_stock_data("POST", "post_stock.csv")

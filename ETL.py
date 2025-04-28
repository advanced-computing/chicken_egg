from clean_birds import clean_bird_flu_data                   # your CDC bird-flu scraper + cleaner
from app_bigquery.clean_egg_prices import clean_egg_price_data         # your egg-price cleaner
from app_bigquery.clean_stocks import fetch_stock_data
from app_bigquery.clean_wild_birds import clean_wild_birds

from upload_to_bigquery import main as upload_to_bigquery


def main():
    print("Starting ETL process…")

    print("Cleaning bird-flu (commercial) data…")
    # should read CDC page, clean and write to app_data/prep_data/bird_flu_daily.csv
    clean_bird_flu_data()

    print("Cleaning egg-price data…")
    # should read the FRED/GitHub CSV, clean and write to app_data/prep_data/egg_price_monthly.csv
    clean_egg_price_data()

    print("Cleaning stock-price data…")
    # should pull CALM, POST, VITL, clean and write to
    #   app_data/prep_data/{calmaine,post,vitl}_prices_daily.csv
    fetch_stock_data()

    print("Cleaning wild-bird HPAI data…")
    # should read the USDA/Socrata feed, clean and write to app_data/prep_data/wild_birds.csv
    clean_wild_birds()

    print("All cleaning done. Now uploading to BigQuery…")
    upload_to_bigquery()

    print("🎉 ETL complete.")

if __name__ == "__main__":
    main()
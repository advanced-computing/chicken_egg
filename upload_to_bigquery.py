# upload_to_bigquery.py


import os
# Path set to Google Cloud Account
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"


from app_bigquery.upload_wild_birds import upload_wild_birds_data
from app_bigquery.upload_bird_flu import upload_bird_flu_data
from app_bigquery.upload_egg_prices import upload_egg_prices_data
from app_bigquery.upload_stock_prices import upload_stock_prices_data

def main():
    project_id = os.getenv("GCP_PROJECT_ID", "sipa-adv-c-arnav-fred")
    
    print("Starting upload to BigQuery...")
    
    upload_wild_birds_data(project_id)
    upload_bird_flu_data(project_id)
    upload_egg_prices_data(project_id)
    
    stock_files = {
        "calmaine": "app_data/calmaine_stock.csv",
        "post": "app_data/post_stock.csv",
        "vitl": "app_data/vitl_stock.csv"
    }
    
    for stock_name, stock_file in stock_files.items():
        print(f"   • uploading {stock_name}…")
        upload_stock_prices_data(project_id, stock_file, stock_name)

    print("All datasets uploaded successfully to BigQuery.")

if __name__ == "__main__":
    main()

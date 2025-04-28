# wild bird function
import os
import pandas as pd
from google.cloud import bigquery
from pandas_gbq import to_gbq, gbq
from google.oauth2 import service_account

def upload_wild_birds_data(project_id: str):
    dataset_id = "chicken_egg"
    table_name = "wild_birds"
    csv_path = "app_data/prep_data/wild_birds.csv"
    full_table_id = f"{project_id}.{dataset_id}.{table_name}"

    schema = [
        bigquery.SchemaField("State", "STRING"),
        bigquery.SchemaField("County", "STRING"),
        bigquery.SchemaField("Date Detected", "DATE"),
        bigquery.SchemaField("Bird Species", "STRING"),
    ]

     # load the JSON key from the env var
    creds = service_account.Credentials.from_service_account_file(
         os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
     )
    client = bigquery.Client(project=project_id, credentials=creds)

    
    df = pd.read_csv(csv_path)
    df["Date Detected"] = pd.to_datetime(df["Date Detected"], errors="coerce")
    df = df[["State", "County", "Date Detected", "Bird Species"]]
    
    
        # --- Incremental loading ---
    # If the table already has data, find the latest date
    try:
        # Query the maximum date present in the table.
        query = f"SELECT MAX(`Date Detected`) as max_date FROM `{full_table_id}`"
        result_df = client.query(query).to_dataframe()
        max_date = result_df["max_date"].iloc[0]
        if pd.notnull(max_date):
            max_date = pd.to_datetime(max_date)
            before_filtering = len(df)
            df = df[df["Date Detected"] > max_date]
            print(f"Found max date in table: {max_date}. Filtered out {before_filtering - len(df)} old records.")
        else:
            print("No previous records found.")
    except Exception as e:
        print("Error checking for existing records, will attempt to append all:", e)
    

    try:
        client.get_table(full_table_id)
        print(f"Table '{full_table_id}' already exists.")
    except Exception:
        table = bigquery.Table(full_table_id, schema=schema)
        client.create_table(table)
        print(f"Table '{full_table_id}' created.")

    
    try:
        print(f"Trying to append to table: {full_table_id}")
        to_gbq(df, full_table_id, project_id=project_id, if_exists="append")
        print(f"Appended {len(df)} records to BigQuery.")
    except gbq.InvalidSchema:
        print("Schema mismatch detected. Replacing table instead...")
        to_gbq(df, full_table_id, project_id=project_id, if_exists="replace")
        print(f"Replaced table and uploaded {len(df)} records.")
    print(f"Uploaded {len(df)} records to BigQuery.")

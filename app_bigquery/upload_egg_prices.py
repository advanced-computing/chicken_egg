# egg prices function

import pandas as pd
from google.cloud import bigquery
from pandas_gbq import to_gbq, gbq
import streamlit as st
from google.oauth2 import service_account

def upload_egg_prices_data(project_id: str):
    dataset_id = "chicken_egg"
    table_name = "egg_prices"
    csv_path = "app_data/cleaned_egg_prices.csv"
    full_table_id = f"{project_id}.{dataset_id}.{table_name}"

    schema = [
        bigquery.SchemaField("Date", "DATE"),
        bigquery.SchemaField("Avg_Price", "FLOAT")
    ]
    
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    client = bigquery.Client(project=project_id, credentials=credentials)

    try:
        client.get_table(full_table_id)
        print(f"Table '{full_table_id}' already exists.")
    except Exception:
        table = bigquery.Table(full_table_id, schema=schema)
        client.create_table(table)
        print(f"Table '{full_table_id}' created.")

    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df[["Avg_Price", "Date"]]
    
        # --- Incremental Loading ---
    # Query the maximum date already in the table.
    try:
        query = f"SELECT MAX(Date) as max_date FROM `{full_table_id}`"
        result_df = client.query(query).to_dataframe()
        max_date = result_df["max_date"].iloc[0]
        if pd.notnull(max_date):
            max_date = pd.to_datetime(max_date)
            before_filtering = len(df)
            df = df[df["Date"] > max_date]
            print(f"Found max date in table: {max_date}. Filtered out {before_filtering - len(df)} old records.")
        else:
            print("No previous records found.")
    except Exception as e:
        print("Error checking for existing records, will attempt to append all:", e)

    
    try:
        print(f"Trying to append: {len(df)} records to table: {full_table_id}")
        to_gbq(df, full_table_id, project_id=project_id, if_exists="append")
        print(f"Appended {len(df)} records to BigQuery.")
    except gbq.InvalidSchema:
        print("Schema mismatch detected. Replacing table instead...")
        to_gbq(df, full_table_id, project_id=project_id, if_exists="replace")
        print(f"Replaced table and uploaded {len(df)} records.")
    print(f"Uploaded {len(df)} records to BigQuery.")

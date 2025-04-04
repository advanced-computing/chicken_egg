# stock prices

import pandas as pd
from google.cloud import bigquery
from pandas_gbq import to_gbq, gbq

def upload_stock_prices_data(project_id: str, stock_file: str, table_name: str):
    dataset_id = "chicken_egg"
    csv_path = stock_file
    full_table_id = f"{project_id}.{dataset_id}.{table_name}"

    schema = [
        bigquery.SchemaField("Date", "DATE"),
        bigquery.SchemaField("Open", "FLOAT"),
        bigquery.SchemaField("High", "FLOAT"),
        bigquery.SchemaField("Low", "FLOAT"),
        bigquery.SchemaField("Close_Last", "FLOAT"),
        bigquery.SchemaField("Volume", "INTEGER")
    ]

    client = bigquery.Client(project=project_id)

    try:
        client.get_table(full_table_id)
        print(f"Table '{full_table_id}' already exists.")
    except Exception:
        table = bigquery.Table(full_table_id, schema=schema)
        client.create_table(table)
        print(f"Table '{full_table_id}' created.")

    df = pd.read_csv(csv_path)
    # Clean "$" if present
    for col in ["Open", "High", "Low", "Close/Last"]:
        if df[col].dtype == object:
            df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.rename(columns={"Close/Last": "Close_Last"}, inplace=True)

    try:
        print(f"Trying to append to table: {full_table_id}")
        to_gbq(df, full_table_id, project_id=project_id, if_exists="append")
        print(f"Appended {len(df)} records to BigQuery.")
    except gbq.InvalidSchema:
        print("Schema mismatch detected. Replacing table instead...")
        to_gbq(df, full_table_id, project_id=project_id, if_exists="replace")
        print(f"Replaced table and uploaded {len(df)} records.")
    print(f"Uploaded {len(df)} records to BigQuery.")

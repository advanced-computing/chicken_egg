# bird flu

import pandas as pd
from google.cloud import bigquery
from pandas_gbq import to_gbq, gbq

def upload_bird_flu_data(project_id: str):
    dataset_id = "chicken_egg"
    table_name = "bird_flu"
    csv_path = "app_data/prep_data/bird_flu.csv"
    full_table_id = f"{project_id}.{dataset_id}.{table_name}"

    schema = [
        bigquery.SchemaField("State", "STRING"),
        bigquery.SchemaField("County", "STRING"),
        bigquery.SchemaField("Flock Size", "INTEGER"),
        bigquery.SchemaField("Flock Type", "STRING"),
        bigquery.SchemaField("Date", "DATE")
    ]

    client = bigquery.Client(project=project_id)

    try:
        client.get_table(full_table_id)
        print(f"✅ Table '{full_table_id}' already exists.")
    except Exception:
        table = bigquery.Table(full_table_id, schema=schema)
        client.create_table(table)
        print(f"📦 Table '{full_table_id}' created.")

    df = pd.read_csv(csv_path)
    df["Outbreak Date"] = pd.to_datetime(df["Outbreak Date"], errors="coerce")
    try:
        print(f"📤 Trying to append to table: {full_table_id}")
        to_gbq(df, full_table_id, project_id=project_id, if_exists="append")
        print(f"✅ Appended {len(df)} records to BigQuery.")
    except gbq.InvalidSchema as e:
        print("⚠️ Schema mismatch detected. Replacing table instead...")
        to_gbq(df, full_table_id, project_id=project_id, if_exists="replace")
        print(f"✅ Replaced table and uploaded {len(df)} records.")
    print(f"✅ Uploaded {len(df)} records to BigQuery.")



from google.cloud import bigquery
import pandas as pd
import streamlit as st
from google.oauth2 import service_account


creds = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(creds)

# Initializing bigquery
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


@st.cache_data(ttl=3600)
def query_table(table_name: str, columns: str = "*", project_id="sipa-adv-c-arnav-fred") -> pd.DataFrame:
    

    # Fetch all schema fields from BigQuery if columns is None
    if columns is None:
        table_ref = f"{project_id}.chicken_egg.{table_name}"
        table = client.get_table(table_ref)
        columns = [field.name for field in table.schema]

    # Safety check: ensure all requested columns exist in the table
    else:
        table_ref = f"{project_id}.chicken_egg.{table_name}"
        table = client.get_table(table_ref)
        all_columns = [field.name for field in table.schema]
        missing = [col for col in columns if col not in all_columns]
        if missing:
            raise ValueError(f"Columns not found in table {table_name}: {missing}")
    
    select_clause = ", ".join([f"`{col}`" for col in columns])
    query = f"SELECT {select_clause} FROM `sipa-adv-c-arnav-fred.chicken_egg.{table_name}`"
    return client.query(query).to_dataframe(create_bqstorage_client=False)


def main():
    st.title("BigQuery Test")

    table = st.selectbox("Select a table:", ["wild_birds", "bird_flu", "egg_prices"])
    df = query_table(table)
    st.write(df.head(10))


if __name__ == "__main__":
    main()

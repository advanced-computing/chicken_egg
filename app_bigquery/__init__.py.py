# upload_to_bigquery.py
#

import pandas as pd
from pandas_gbq import to_gbq
from google.cloud import bigquery

# === CONFIGURA ESTO ===
project_id = "tu-proyecto-id"  # Reemplaza esto si ya tienes un project ID
dataset_id = "chicken_egg"
table_name = "wild_birds"
csv_path = "app_data/prep_data/wild_birds.csv"
full_table_id = f"{project_id}.{dataset_id}.{table_name}"

# === Autenticación (opcional si ya hiciste `gcloud auth login`)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# === Crea la tabla si no existe ===
client = bigquery.Client(project=project_id)

schema = [
    bigquery.SchemaField("State", "STRING"),
    bigquery.SchemaField("County", "STRING"),
    bigquery.SchemaField("Date Detected", "DATE"),
    bigquery.SchemaField("Bird Species", "STRING"),
    bigquery.SchemaField("lat", "FLOAT"),
    bigquery.SchemaField("lng", "FLOAT")
]

try:
    client.get_table(full_table_id)
    print(f"✅ La tabla '{full_table_id}' ya existe.")
except Exception:
    table = bigquery.Table(full_table_id, schema=schema)
    client.create_table(table)
    print(f"📦 Tabla '{full_table_id}' creada.")

# === Cargar y subir CSV ===
df = pd.read_csv(csv_path)

# 💡 Si haces carga incremental, aquí iría la lógica para filtrar nuevos datos

# Subida de datos
to_gbq(df, full_table_id, project_id=project_id, if_exists="append")
print(f"✅ Se subieron {len(df)} registros a BigQuery.")
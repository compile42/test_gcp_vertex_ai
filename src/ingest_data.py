import pandas as pd
import numpy as np
from google.cloud import bigquery

# Configuration
PROJECT_ID = "project-440bdad3-9821-4677-939"
DATASET_ID = "churn_analysis"
TABLE_ID = "customers_data"
REGION = "europe-west1"

client = bigquery.Client(project=PROJECT_ID, location=REGION)

def generate_churn_data(n_clients=2000):
    print(f"Génération de {n_clients} clients fictifs...")
    np.random.seed(42)
    
    data = pd.DataFrame({
        'customer_id': [f"CUST_{i:05d}" for i in range(n_clients)],
        'age': np.random.randint(18, 80, n_clients),
        'anciennete_mois': np.random.randint(1, 72, n_clients),
        'facture_mensuelle': np.random.uniform(20, 150, n_clients),
        'nb_reclamations': np.random.randint(0, 12, n_clients),
        'churn': np.random.choice([0, 1], n_clients, p=[0.85, 0.15]) # 15% de départ
    })
    return data

def upload_to_bigquery(df):
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    
    print(f"Envoi des données vers BigQuery ({table_ref})...")
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result() 
    print("Succès ! Les données sont dans BigQuery.")

if __name__ == "__main__":
    df_churn = generate_churn_data()
    upload_to_bigquery(df_churn)

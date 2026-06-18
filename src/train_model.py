import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from google.cloud import bigquery
from google.cloud import storage
import joblib
import os

# Configuration (Vertex AI injecte souvent ces infos via variables d'env)
PROJECT_ID = "project-440bdad3-9821-4677-939"
BUCKET_NAME = f"{PROJECT_ID}-vertex-artifacts"

print("1. Lecture des données depuis BigQuery...")
client = bigquery.Client(project=PROJECT_ID)
query = f"SELECT * FROM `churn_analysis.customers_data`"
df = client.query(query).to_dataframe()

# Préparation simple
X = df[['age', 'anciennete_mois', 'facture_mensuelle', 'nb_reclamations']]
y = df['churn']

print("2. Entraînement du modèle...")
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

print("3. Sauvegarde du modèle vers Cloud Storage...")
model_filename = "model.joblib"
joblib.dump(model, model_filename)

# Envoi vers le bucket créé par Terraform
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(f"model_outputs/{model_filename}")
blob.upload_from_filename(model_filename)

print(f"Modèle sauvegardé dans gs://{BUCKET_NAME}/model_outputs/{model_filename}")

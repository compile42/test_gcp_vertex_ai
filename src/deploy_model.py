from google.cloud import aiplatform

PROJECT_ID = "project-440bdad3-9821-4677-939"
REGION = "europe-west1"
BUCKET_NAME = f"{PROJECT_ID}-vertex-artifacts"

# 1. Initialisation du SDK Vertex AI
aiplatform.init(project=PROJECT_ID, location=REGION)

print("1. Enregistrement du modèle dans le Vertex Model Registry...")
model = aiplatform.Model.upload(
    display_name="churn-random-forest",
    # On lui pointe le DOSSIER où est stocké le fichier joblib
    artifact_uri=f"gs://{BUCKET_NAME}/model_outputs/",
    # On lui donne l'image Docker officielle de Google pour le "serving" (la prédiction)
    serving_container_image_uri="europe-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-23:latest"
)

print(f"Modèle enregistré avec succès ! ID: {model.resource_name}")

print("2. Création de l'Endpoint...")
# On crée d'abord la boîte (l'Endpoint)
endpoint = aiplatform.Endpoint.create(
    display_name="churn-api-endpoint",
    project=PROJECT_ID,
    location=REGION
)

print(f"Endpoint créé avec succès ! Resource name: {endpoint.resource_name}")

print("3. Déploiement du modèle sur l'Endpoint...")
# Ensuite, on déploie le modèle dans cette boîte
model.deploy(
    endpoint=endpoint,
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=1
)

print(f"API en ligne ! Tu peux envoyer tes requêtes sur l'Endpoint : {endpoint.resource_name}")
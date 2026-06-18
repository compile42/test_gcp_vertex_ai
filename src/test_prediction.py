from google.cloud import aiplatform

PROJECT_ID = "project-440bdad3-9821-4677-939"
REGION = "europe-west1"
# On reprend l'ID de ton Endpoint actif que tu viens de m'envoyer
ENDPOINT_ID = "6440088093511909376"

# 1. Connexion à l'Endpoint
aiplatform.init(project=PROJECT_ID, location=REGION)
endpoint = aiplatform.Endpoint(ENDPOINT_ID)

# 2. Définition des profils clients à tester
# Le modèle attend dans l'ordre : [age, anciennete_mois, facture_mensuelle, nb_reclamations]
profil_client_1 = [[25, 48, 30.0, 0]]  # Jeune, fidèle, petite facture, 0 réclamation (Normalement reste)
profil_client_2 = [[62, 3, 145.0, 10]] # Nouveau, grosse facture, énormément de réclamations (Risque élevé)

print("Envoi des données à l'Endpoint Vertex AI...")

# 3. Appel de l'API
response_1 = endpoint.predict(instances=profil_client_1)
response_2 = endpoint.predict(instances=profil_client_2)

print("\n--- RÉSULTATS DES PRÉDICTIONS ---")
print(f"Client 1 (Fidèle) : Résultat = {response_1.predictions}")
print(f"Client 2 (Frustré) : Résultat = {response_2.predictions}")
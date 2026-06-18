# terraform/main.tf

variable "project_id" {
  description = "L'ID de votre projet GCP"
  type        = string
}

variable "region" {
  description = "La région pour vos ressources"
  type        = string
  default     = "us-central1"
}

# On retire la partie "google_project_service" car vous n'avez pas les droits
# pour gérer les APIs depuis Terraform dans ce projet.

# 1. Bucket pour les artefacts ML
resource "google_storage_bucket" "ml_artifacts" {
  name                        = "${var.project_id}-vertex-artifacts"
  location                    = var.region
  project                     = var.project_id
  uniform_bucket_level_access = true
  force_destroy               = true
}

# 2. Dataset BigQuery pour vos données de Churn
resource "google_bigquery_dataset" "churn_data" {
  dataset_id                  = "churn_analysis"
  friendly_name               = "Churn Analysis Dataset"
  description                 = "Dataset contenant les données d'entraînement pour le modèle de Churn"
  location                    = var.region
  project                     = var.project_id
  delete_contents_on_destroy = true
}

# 3. Artifact Registry pour vos images Docker
resource "google_artifact_registry_repository" "ml_images" {
  location      = var.region
  repository_id = "ml-pipelines-repo"
  description   = "Dépôt Docker pour les pipelines Vertex AI"
  format        = "DOCKER"
  project       = var.project_id
}

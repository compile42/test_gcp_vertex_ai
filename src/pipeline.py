from kfp import dsl
from kfp import compiler
from google.cloud import aiplatform

# Configurations globales
PROJECT_ID = "project-440bdad3-9821-4677-939"
REGION = "europe-west1"
BUCKET_NAME = f"gs://{PROJECT_ID}-vertex-artifacts"

# L'image de ton projet stockée dans l'Artifact Registry (construite via ta CI/CD)
BASE_IMAGE = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/ml-pipelines-repo/churn-project:latest"

# =====================================================================
# ÉTAPE 1 : Définition des composants basés sur ton conteneur
# =====================================================================

@dsl.container_component
def ingest_data_op():
    return dsl.ContainerSpec(
        image=BASE_IMAGE,
        command=["python", "ingest_data.py"] # Appel direct à ton fichier existant
    )

@dsl.container_component
def train_model_op():
    return dsl.ContainerSpec(
        image=BASE_IMAGE,
        command=["python", "train_model.py"] # Appel direct à ton fichier existant
    )

@dsl.container_component
def deploy_model_op():
    return dsl.ContainerSpec(
        image=BASE_IMAGE,
        command=["python", "deploy_model.py"] # Appel direct à ton fichier existant
    )

# =====================================================================
# ÉTAPE 2 : Définition du Graph (Le DAG)
# =====================================================================

@dsl.pipeline(
    name="churn-industrial-pipeline",
    description="Pipeline MLOps modulaire utilisant des conteneurs personnalisés",
    pipeline_root=BUCKET_NAME
)
def churn_ml_pipeline():
    # 1. Ingestion
    ingest_task = ingest_data_op()
    
    # 2. Entraînement
    train_task = train_model_op()
    train_task.after(ingest_task)
    
    # 3. Déploiement
    deploy_task = deploy_model_op()
    deploy_task.after(train_task)

# =====================================================================
# ÉTAPE 3 : Compilation et Lancement
# =====================================================================

if __name__ == "__main__":
    pipeline_spec_file = "churn_pipeline.json"
    compiler.Compiler().compile(
        pipeline_func=churn_ml_pipeline,
        package_path=pipeline_spec_file
    )
    
    aiplatform.init(project=PROJECT_ID, location=REGION)
    
    pipeline_job = aiplatform.PipelineJob(
        display_name="churn-pipeline-containers-run",
        template_path=pipeline_spec_file,
        enable_caching=True
    )
    
    pipeline_job.submit()
    print("Pipeline industriel soumis avec succès !")
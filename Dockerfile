FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances globales du projet
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tous tes scripts (ingest_data.py, train_model.py, etc.)
COPY src/ .

# Pas de CMD ! C'est Kubeflow qui choisira quel script lancer (command=["python", "xxx.py"])
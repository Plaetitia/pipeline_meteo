import json
import os
from datetime import datetime
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

# Configuration des accès via les variables d'environnement
API_KEY = os.getenv("METEO_API_KEY")
API_URL = os.getenv("METEO_API_URL")

default_args = {
    "owner": "laetitia",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

def fetch_meteo_lille():
    # Appel API Météo-France
    params = {"id_station": "59343001", "format": "json"}
    headers = {"apikey": API_KEY, "accept": "application/json"}
    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    print(f"Données reçues : {data}")

    if data:
        # Chemin du dossier partagé accessible par Airflow et Spark
        output_dir = "/opt/airflow/src/data"
        os.makedirs(output_dir, exist_ok=True)
        
        # Enregistrement en tant que fichier JSON unique ou fichier fixe que Spark lit
        filepath = os.path.join(output_dir, "meteo_raw.json")
        
        with open(filepath, "w") as f:
            json.dump(data, f)
            
        print(f"Fichier sauvegardé localement pour Spark : {filepath}")
    else:
        print("Pas de données disponibles")

with DAG(
    "collect_meteo_lille",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    task_get_meteo = PythonOperator(
        task_id="fetch_meteo_lille",
        python_callable=fetch_meteo_lille,
    )
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import requests
import json

# Configuration via variables d'environnement Docker
API_KEY = os.getenv('METEO_API_KEY')
API_URL = os.getenv('METEO_API_URL')
OUTPUT_DIR = "/opt/airflow/data/raw"

default_args = {
    'owner': 'laetitia',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

def fetch_meteo_lille():
    params = {'id_station': '59351002', 'referentiel': 'DATE_ISO'}
    headers = {'Authorization': f'Bearer {API_KEY}', 'accept': 'application/json'}
    
    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_path = f"{OUTPUT_DIR}/meteo_lille_{timestamp}.json"
    
    with open(file_path, 'w') as f:
        json.dump(response.json(), f)
    print(f"Fichier créé : {file_path}")

with DAG(
    'collecte_meteo_lille',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False
) as dag:

    task_get_meteo = PythonOperator(
        task_id='fetch_meteo_lille',
        python_callable=fetch_meteo_lille,
    )

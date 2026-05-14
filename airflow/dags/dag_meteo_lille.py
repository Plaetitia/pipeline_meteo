from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import requests
import json
import boto3
from botocore.client import Config

# Configuration
API_KEY = os.getenv('METEO_API_KEY')
API_URL = os.getenv('METEO_API_URL')

default_args = {
    'owner': 'laetitia',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

def fetch_meteo_lille():
    # Appel API
    params = {'id_station': '59343001', 'format': 'json'}
    headers = {'apikey': API_KEY, 'accept': 'application/json'}
    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    print(f"Données reçues : {data}")

    if data:
        # Connexion MinIO
        s3 = boto3.client(
            's3',
            endpoint_url='http://minio:9000',
            aws_access_key_id='admin',
            aws_secret_access_key='password',
            config=Config(signature_version='s3v4')
        )

        # Envoi vers MinIO
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"meteo_lille_{timestamp}.json"
        s3.put_object(
            Bucket='meteo-donnees',
            Key=filename,
            Body=json.dumps(data)
        )
        print(f"Fichier envoyé dans MinIO : {filename}")
    else:
        print("Pas de données disponibles")

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
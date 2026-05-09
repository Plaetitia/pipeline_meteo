import os
import time
import json
import requests
from kafka import KafkaProducer
from dotenv import load_dotenv

# Charger les variables du .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# ID de la station météo (Paris-Montsouris)
STATION_ID = "75114001"

def get_meteo_data():
    """Récupère les données depuis l'API Météo-France"""
    url = f"https://public-api.meteofrance.fr/public/DPObs/v1/station/infrahoraire-6m"
    headers = {
        "apikey": API_KEY
    }
    params = {
        "id_station": STATION_ID,
        "format": "json"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur API: {response.status_code} - {response.text}")
        return None

def send_to_kafka(producer, data):
    """Envoie les données vers Kafka"""
    producer.send(KAFKA_TOPIC, value=data)
    producer.flush()
    print(f"Données envoyées vers Kafka : {data}")

def main():
    # Connexion à Kafka
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    print("Producer démarré, collecte des données...")

    while True:
        data = get_meteo_data()
        if data:
            send_to_kafka(producer, data)
        # Attendre 6 minutes (fréquence de l'API)
        time.sleep(360)

if __name__ == "__main__":
    main()
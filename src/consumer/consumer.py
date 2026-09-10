import os
import json
import boto3
from kafka import KafkaConsumer
from dotenv import load_dotenv
from botocore.client import Config

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "meteo_topic")

def save_to_minio(data):
    """Sauvegarde les données dans MinIO"""
    s3 = boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id='admin',
        aws_secret_access_key='password',
        config=Config(signature_version='s3v4')
    )
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"meteo_{timestamp}.json"
    s3.put_object(
        Bucket='meteo-donnees',
        Key=filename,
        Body=json.dumps(data)
    )
    print(f"Sauvegardé dans MinIO : {filename}")

def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="meteo_group"
    )

    print("Consumer démarré, en attente de messages...")

    for message in consumer:
        data = message.value
        print(f"Message reçu : {data}")
        save_to_minio(data)

if __name__ == "__main__":
    main()
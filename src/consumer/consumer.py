import os
import json
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

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
        # TODO: sauvegarder dans HDFS

if __name__ == "__main__":
    main()
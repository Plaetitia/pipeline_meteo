from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def process():
    # 1. Créer la session Spark avec le driver JDBC PostgreSQL inclus
    spark = SparkSession.builder \
        .appName("MeteoTransformation") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
        .getOrCreate()

    # 2. Source des données : 
    # (Si ton étape précédente enregistre un fichier JSON dans un dossier local partagé, par exemple /opt/airflow/src/data/raw.json)
    # Ajuste ce chemin selon l'endroit où l'API sauvegarde les données brutes.
    input_path = "/opt/airflow/src/data/meteo_raw.json" 
    
    try:
        df = spark.read.json(input_path)
    except Exception as e:
        print(f"Aucun fichier trouvé à lire pour l'instant : {e}")
        return

    # 3. Nettoyage et Transformation (on filtre uniquement sur les colonnes clés si elles sont nulles)
    df_filtered = df.dropna(subset=["validity_time", "t"]).filter(col("t") > -50)

    # 4. Écriture directe dans PostgreSQL
    # Les identifiants correspondent à ton fichier .env / docker-compose
    postgres_url = "jdbc:postgresql://postgres:5432/airflow"
    postgres_properties = {
        "user": "airflow",
        "password": "airflow", # Remplace par ta variable si besoin
        "driver": "org.postgresql.Driver"
    }

    df_filtered.write \
        .jdbc(url=postgres_url, table="meteo_lille", mode="append", properties=postgres_properties)

    print("Traitement Spark terminé et données insérées dans PostgreSQL !")

if __name__ == "__main__":
    process()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Créer la session Spark
spark = SparkSession.builder \
    .appName("MeteoTransformation") \
    .getOrCreate()

# Schéma des données météo
schema = StructType([
    StructField("id_station", StringType()),
    StructField("temperature", DoubleType()),
    StructField("humidite", DoubleType()),
    StructField("vent", DoubleType()),
    StructField("pression", DoubleType()),
    StructField("date", StringType())
])

def process():
    # Lire depuis HDFS
    df = spark.read.json("hdfs://namenode:9000/meteo/raw/")

    # Nettoyage : supprimer les lignes vides
    df_clean = df.dropna()

    # Transformation : filtrer temperature > -50
    df_filtered = df_clean.filter(col("temperature") > -50)

    # Sauvegarder dans HDFS (données propres)
    df_filtered.write.mode("overwrite") \
        .parquet("hdfs://namenode:9000/meteo/clean/")

    print("Traitement Spark terminé !")

if __name__ == "__main__":
    process()
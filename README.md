# pipeline_meteo
Projet  de déploiement de pipeline Big Data - Hadoop
## Sujet
Pipeline Big Data qui collecte les données météo en temps réel
depuis l'API Météo-France (station de Lille), les ingère via Kafka,
les traite avec Spark et les stocke dans PostgreSQL.
Le pipeline est orchestré par Apache Airflow et déployé via GitLab CI/CD.

# Architecture
API Météo-France ->Kafka -> HDFS -> Spark  ->  PostgreSQL -> Airflow (orchestration ETL)
## Technologies
- **Apache Kafka** : ingestion des flux temps réel
- **Apache Spark** : traitement distribué
- **HDFS** : stockage Data Lake
- **PostgreSQL** : stockage final pour analyse
- **Apache Airflow** : orchestration ETL
- **Docker** : conteneurisation
- **GitLab CI/CD** : intégration et déploiement continus

## Structure du projet
pipeline_meteo/
    airflow/
        dags/
            dag_meteo_lille.py  # DAG Airflow
src/
    producer/    # Collecte API → Kafka
    consumer/    # Kafka → HDFS
    spark/       # Traitement Spark
sql/             # Scripts PostgreSQL
scripts/         # Scripts utilitaires
.gitlab-ci.yml   # Pipeline CI/CD
docker-compose.yml
.env
requirements.txt


## Les instructions de lancement

### 1 - Prérequis
- Docker Desktop installé
- Python 3.12+
- Compte GitLab avec Runner configuré

### 2 - Configuration
```bash
git clone https://github.com/Plaetitia/pipeline_meteo.git
cd pipeline_meteo
cp .env.example .env
# Remplir API_KEY et autres valeurs dans .env
```

### 3 - Lancer les services Docker
```bash
docker-compose up -d
```

### 4 - Lancer le producer
```bash
source Env/bin/activate
python src/producer/producer.py
```

### 5 - Lancer le consumer
```bash
python src/consumer/consumer.py
```

### 6 - Lancer le job Spark
```bash
python src/spark/spark_job.py
```

### 7 - CI/CD GitLab
Le pipeline se déclenche automatiquement à chaque push sur `main`.
Il lance `docker-compose up -d` via le Runner GitLab.
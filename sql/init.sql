-- Création de la table des observations météo
CREATE TABLE IF NOT EXISTS observations (
    id SERIAL PRIMARY KEY,
    id_station VARCHAR(20),
    temperature FLOAT,
    humidite FLOAT,
    vent FLOAT,
    pression FLOAT,
    date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Index pour accélérer les recherches
CREATE INDEX IF NOT EXISTS idx_station ON observations(id_station);
CREATE INDEX IF NOT EXISTS idx_date ON observations(date);
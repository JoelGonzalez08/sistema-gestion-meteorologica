CREATE TABLE IF NOT EXISTS weather_logs (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50) NOT NULL,
    temperature REAL,
    humidity REAL,
    pressure REAL,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
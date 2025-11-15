from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import pool
import os
import time

# --- Configuración de la Base de Datos ---
def get_db_pool():
    while True:
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(1, 5,
                host=os.getenv('POSTGRES_HOST'),
                database=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'))
            print("API: Pool de conexiones a PostgreSQL creado.")
            return db_pool
        except psycopg2.OperationalError as e:
            print(f"API: No se pudo conectar a PostgreSQL: {e}. Reintentando...")
            time.sleep(5)

app = FastAPI(title="API de Logs Meteorológicos")
db_pool = get_db_pool()

@app.get("/logs/")
def get_weather_logs(limit: int = 10):
    """Obtiene los últimos N registros de logs meteorológicos."""
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute("SELECT id, station_id, temperature, humidity, pressure, timestamp FROM weather_logs ORDER BY timestamp DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
            # Convertir tuplas a diccionarios para una respuesta JSON amigable
            result = [dict(zip([column.name for column in cur.description], row)) for row in rows]
            return result
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        if conn:
            db_pool.putconn(conn)

@app.get("/logs/{station_id}")
def get_station_logs(station_id: str, limit: int = 10):
    """Obtiene los últimos N registros para una estación específica."""
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute("SELECT id, station_id, temperature, humidity, pressure, timestamp FROM weather_logs WHERE station_id = %s ORDER BY timestamp DESC LIMIT %s", (station_id, limit))
            rows = cur.fetchall()
            result = [dict(zip([column.name for column in cur.description], row)) for row in rows]
            return result
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        if conn:
            db_pool.putconn(conn)

@app.get("/health")
def health_check():
    return {"status": "ok"}
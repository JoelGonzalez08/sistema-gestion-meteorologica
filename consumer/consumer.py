import pika
import json
import psycopg2
from psycopg2 import pool
import time
import os

def get_db_pool():
    while True:
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
                host=os.getenv('POSTGRES_HOST'),
                database=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'))
            print("Pool de conexiones a PostgreSQL creado exitosamente.")
            return db_pool
        except psycopg2.OperationalError as e:
            print(f"No se pudo conectar a PostgreSQL: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

def process_message(ch, method, properties, body, db_pool):
    try:
        data = json.loads(body)
        print(f" [x] Recibido: {data}")

        # Validación de datos
        if not (-50 < data['temperature'] < 60 and 0 <= data['humidity'] <= 100):
            print(f" [!] Datos inválidos recibidos: {data}. Descartando mensaje.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO weather_logs (station_id, temperature, humidity, pressure, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (data['station_id'], data['temperature'], data['humidity'], data['pressure'], data['timestamp'])
            )
            conn.commit()
        db_pool.putconn(conn)
        print(" [x] Datos guardados en PostgreSQL.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except (json.JSONDecodeError, KeyError) as e:
        print(f" [!] Error de formato en el mensaje: {e}. Descartando.")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except psycopg2.Error as e:
        print(f" [!] Error de base de datos: {e}. Devolviendo mensaje a la cola.")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        # Podríamos cerrar la conexión si es un error grave
    except Exception as e:
        print(f" [!] Error inesperado: {e}. Devolviendo mensaje a la cola.")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
    db_pool = get_db_pool()
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=600, blocked_connection_timeout=300))
            channel = connection.channel()
            channel.exchange_declare(exchange='weather_exchange', exchange_type='direct', durable=True)
            channel.queue_declare(queue='weather_queue', durable=True)
            channel.queue_bind(exchange='weather_exchange', queue='weather_queue', routing_key='weather_logs')

            channel.basic_qos(prefetch_count=1)
            
            on_message_callback = lambda ch, method, properties, body: process_message(ch, method, properties, body, db_pool)
            channel.basic_consume(queue='weather_queue', on_message_callback=on_message_callback)

            print(' [*] Esperando mensajes. Para salir presiona CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("Conexión con RabbitMQ perdida. Reintentando en 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Cerrando consumidor.")
            if connection and not connection.is_closed:
                connection.close()
            db_pool.closeall()
            break

if __name__ == '__main__':
    main()
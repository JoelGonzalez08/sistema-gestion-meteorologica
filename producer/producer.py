import pika
import json
import time
import random
import os

def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='rabbitmq', heartbeat=600, blocked_connection_timeout=300)
            )
            print("Conexión exitosa con RabbitMQ.")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("No se pudo conectar a RabbitMQ. Reintentando en 5 segundos...")
            time.sleep(5)

def publish_message():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.exchange_declare(exchange='weather_exchange', exchange_type='direct', durable=True)

    while True:
        try:
            data = {
                'station_id': f'station_{random.randint(1, 5)}',
                'temperature': round(random.uniform(-10.0, 40.0), 2),
                'humidity': round(random.uniform(20.0, 100.0), 2),
                'pressure': round(random.uniform(980.0, 1050.0), 2),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            message = json.dumps(data)
            channel.basic_publish(
                exchange='weather_exchange',
                routing_key='weather_logs',
                body=message,
                properties=pika.BasicProperties(delivery_mode=2) # Mensaje persistente
            )
            print(f" [x] Enviado: {message}")
            time.sleep(random.uniform(1.0, 3.0))
        except pika.exceptions.ConnectionClosedByBroker:
            print("Conexión cerrada por el broker. Reintentando...")
            connection = connect_to_rabbitmq()
            channel = connection.channel()
            channel.exchange_declare(exchange='weather_exchange', exchange_type='direct', durable=True)
        except Exception as e:
            print(f"Ocurrió un error: {e}. Reintentando conexión...")
            connection = connect_to_rabbitmq()
            channel = connection.channel()
            channel.exchange_declare(exchange='weather_exchange', exchange_type='direct', durable=True)

if __name__ == '__main__':
    print("Iniciando productor...")
    publish_message()
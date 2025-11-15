import pika
import json
import time

# --- Umbrales de Alerta ---
TEMP_THRESHOLD_HIGH = 35.0
HUMIDITY_THRESHOLD_HIGH = 90.0
# -------------------------

def process_message(ch, method, properties, body):
    try:
        data = json.loads(body)
        station_id = data.get('station_id', 'N/A')
        temperature = data.get('temperature', 0)
        humidity = data.get('humidity', 0)

        if temperature > TEMP_THRESHOLD_HIGH:
            print(f"🔴 ALERTA DE TEMPERATURA ALTA en {station_id}: {temperature}°C")

        if humidity > HUMIDITY_THRESHOLD_HIGH:
            print(f"🔵 ALERTA DE HUMEDAD ALTA en {station_id}: {humidity}%")

        # Confirmamos el mensaje para que se elimine de la cola de alertas
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except (json.JSONDecodeError, KeyError) as e:
        print(f"[!] Error de formato en el mensaje, descartando: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        print(f"[!] Error inesperado, reencolando: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()

            # Aseguramos que el exchange exista
            channel.exchange_declare(exchange='weather_exchange', exchange_type='direct', durable=True)

            # Creamos una cola exclusiva y duradera para este consumidor
            channel.queue_declare(queue='alert_queue', durable=True)

            # Unimos nuestra cola al exchange con la misma routing key
            channel.queue_bind(exchange='weather_exchange', queue='alert_queue', routing_key='weather_logs')

            print(' [*] Servicio de Alertas esperando mensajes.')
            channel.basic_consume(queue='alert_queue', on_message_callback=process_message)
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Conexión con RabbitMQ perdida. Reintentando en 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Cerrando servicio de alertas.")
            break

if __name__ == '__main__':
    main()
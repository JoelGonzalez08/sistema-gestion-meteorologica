#!/bin/bash

# Escala el número de réplicas de un servicio específico.
# Uso: ./scripts/scale.sh <nombre_del_servicio> <numero_de_replicas>
# Ejemplo: ./scripts/scale.sh consumer 3

SERVICE=$1
REPLICAS=$2

if [ -z "$SERVICE" ] || [ -z "$REPLICAS" ]; then
  echo "Error: Faltan argumentos."
  echo "Uso: $0 <nombre_del_servicio> <numero_de_replicas>"
  echo "Ejemplo: $0 consumer 3"
  exit 1
fi

echo "Escalando el servicio '$SERVICE' a $REPLICAS réplicas..."

docker-compose -f .devcontainer/docker-compose.yml up -d --scale $SERVICE=$REPLICAS

echo "Escalado completado."
#!/bin/bash

# ¡ADVERTENCIA! Este script detiene todos los contenedores Y ELIMINA LOS VOLÚMENES DE DATOS.
# Úsalo para resetear completamente el entorno.

echo "Realizando una limpieza completa del entorno..."
echo "Esto eliminará todos los datos de RabbitMQ, PostgreSQL y Grafana."

# El flag -v es el que se encarga de eliminar los volúmenes.
docker-compose -f .devcontainer/docker-compose.yml down -v

echo "Entorno limpiado exitosamente."
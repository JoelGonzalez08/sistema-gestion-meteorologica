#!/bin/bash

# Muestra los logs de los servicios.
# Si se pasa un argumento (ej: ./scripts/logs.sh consumer), muestra solo los logs de ese servicio.
# Si no, muestra los logs de todos los servicios.

echo "Mostrando logs en tiempo real... (Presiona Ctrl+C para salir)"

if [ -z "$1" ]; then
  # Sin argumento, muestra todos los logs
  docker-compose -f .devcontainer/docker-compose.yml logs -f
else
  # Con argumento, muestra los logs del servicio especificado
  docker-compose -f .devcontainer/docker-compose.yml logs -f $1
fi
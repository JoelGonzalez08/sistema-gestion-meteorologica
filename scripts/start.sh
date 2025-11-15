#!/bin/bash

# Este script levanta todos los servicios en modo detached (segundo plano).
# La opción --build reconstruye las imágenes si hay cambios en los Dockerfiles.

echo "Iniciando todos los servicios del sistema meteorológico..."

docker-compose -f .devcontainer/docker-compose.yml up --build -d

echo "Sistema iniciado correctamente. Puedes verificar el estado con 'docker ps'."```
#!/bin/bash

# Este script detiene todos los contenedores definidos en el docker-compose.yml.
# No elimina los volúmenes de datos.

echo "Deteniendo todos los servicios..."

docker-compose -f .devcontainer/docker-compose.yml down

echo "Servicios detenidos."
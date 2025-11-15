FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Copia el requirements.txt global desde la raíz del proyecto
COPY ../requirements.txt /tmp/requirements.txt

# Instala todas las dependencias del proyecto en el entorno de desarrollo
RUN pip install --no-cache-dir -r /tmp/requirements.txt
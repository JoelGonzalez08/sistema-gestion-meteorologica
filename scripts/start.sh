#!/bin/bash

# Este script levanta todos los servicios en modo detached (segundo plano).
# La opción --build reconstruye las imágenes si hay cambios en los Dockerfiles.

echo "Iniciando todos los servicios del sistema meteorológico..."

docker-compose -f .devcontainer/docker-compose.yml up --build -d

echo "Sistema iniciado correctamente. Puedes verificar el estado con 'docker ps'."```

#### **2. `stop.sh` - Para detener todos los servicios**

Este script detendrá los contenedores, pero no eliminará los datos (volúmenes).

**`scripts/stop.sh`**
```bash
#!/bin/bash

# Este script detiene todos los contenedores definidos en el docker-compose.yml.
# No elimina los volúmenes de datos.

echo "Deteniendo todos los servicios..."

docker-compose -f .devcontainer/docker-compose.yml down

echo "Servicios detenidos."
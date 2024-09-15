# Tarea_1_Sistemas_Distribuidos_2024_2
Este proyecto implementa un servidor DNS distribuido utilizando gRPC, con múltiples instancias de Redis para almacenamiento en caché de consultas DNS. Se han implementado políticas de particionado y remoción de la caché utilizando Redis.
cada escenario tiene las configuraciones para cada ecenario
Requisitos
Asegúrate de tener instalados los siguientes componentes en tu máquina antes de ejecutar el proyecto:

Docker y Docker Compose: para manejar la orquestación de los servicios.
Python 3.9+: para correr scripts auxiliares, si deseas correr partes del proyecto sin contenedores.
gRPC: ya está incluido en los Dockerfiles, pero puedes instalar grpcio y grpcio-tools si deseas realizar cambios fuera del entorno de Docker.
Dependencias Python
Flask: Framework web para la API REST.
Redis: Cliente Python para interactuar con Redis.
requests: Para realizar solicitudes HTTP.
gRPC: Para la comunicación entre el cliente y el servidor gRPC.
Instalación y configuración
1. Clonar el repositorio
Clona este proyecto en tu máquina local:

bash
Copiar código

2. Configuración de Redis
El proyecto utiliza varias instancias de Redis para caché distribuida. Las particiones de la caché están configuradas de acuerdo con las direcciones hash de las consultas DNS.

En el archivo docker-compose.yml, puedes ver la configuración de Redis. Cada instancia de Redis tiene su propio puerto asignado. Se utiliza particionado de caché por hash para distribuir las claves entre las instancias.

3. Configuración de políticas de remoción de Redis
Puedes ajustar las políticas de remoción de caché en las instancias de Redis configurando los parámetros de maxmemory y maxmemory-policy en el archivo docker-compose.yml. Ejemplo:

yaml
Copiar código
services:
  redis1:
    environment:
      - ALLOW_EMPTY_PASSWORD=yes
      - REDIS_MAXMEMORY=512mb
      - REDIS_MAXMEMORY_POLICY=allkeys-lru
4. Levantar los contenedores con Docker Compose
Para ejecutar el proyecto, debes levantar todos los servicios (API, gRPC, Redis) con Docker Compose. Desde la raíz del proyecto, ejecuta el siguiente comando:

bash
Copiar código
docker-compose up --build
Esto construirá y ejecutará todos los contenedores, incluyendo:

4 instancias de Redis.
El servidor gRPC.
La API REST.
5. Verificar que los servicios están corriendo
Puedes verificar que los contenedores están corriendo con el siguiente comando:

bash
Copiar código
docker ps
Deberías ver algo como esto:

bash
Copiar código
CONTAINER ID   IMAGE                    COMMAND                  STATUS          PORTS
abc12345       redis:7.4                "redis-server ..."       Up 2 minutes    0.0.0.0:6379->6379/tcp
def67890       grpc_server              "python grpc_server..."  Up 2 minutes    0.0.0.0:50051->50051/tcp
ghi12345       api                      "python app.py"          Up 2 minutes    0.0.0.0:5000->5000/tcp
...
6. Hacer consultas a la API
Una vez que los servicios están corriendo, puedes hacer consultas a la API REST. El endpoint de la API para resolver dominios es:

POST /resolve: Consulta el DNS de un dominio, revisando primero la caché, y si no está en caché, consultará el servidor gRPC.
Ejemplo de solicitud utilizando curl:

bash
Copiar código
curl -X POST http://localhost:5000/resolve -H "Content-Type: application/json" -d '{"domain": "google.com"}'
Ejemplo utilizando Python:

python
Copiar código
import requests

url = 'http://localhost:5000/resolve'
payload = {'domain': 'google.com'}

response = requests.post(url, json=payload)
print(response.json())
7. Probar el rendimiento con un CSV de dominios
El proyecto incluye un script para realizar múltiples consultas a la API utilizando un archivo CSV de dominios. Para ejecutarlo, asegúrate de tener el archivo domains.csv en la ruta especificada, luego corre el script envio.py:

bash
Copiar código
python envio.py
8. Políticas de caché y particionado
El sistema utiliza un particionado basado en el hash del dominio para distribuir las claves DNS entre las instancias de Redis. Se puede configurar el número de particiones (instancias Redis) ajustando el archivo docker-compose.yml.

9. Limpiar los contenedores
Para detener y eliminar los contenedores, puedes ejecutar:

bash
Copiar código
docker-compose down
10. Gráfico de Distribución de Frecuencias de las Consultas
El proyecto incluye un script que genera la distribución de frecuencias de las consultas realizadas desde el dataset CSV y muestra un gráfico:

bash
Copiar código
python grafico_frecuencia.py

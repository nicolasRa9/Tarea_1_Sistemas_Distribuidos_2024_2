# Tarea_1_Sistemas_Distribuidos_2024_2
# Proyecto Distribuido con Redis, gRPC y Flask

## Descripción del Proyecto

Este proyecto es una arquitectura distribuida que utiliza múltiples instancias de Redis para la caché, gRPC para las comunicaciones entre cliente y servidor, y Flask como la API para manejar las solicitudes de DNS. El sistema utiliza un enfoque de particionado hash para distribuir las consultas DNS entre varias instancias de Redis, y almacena las respuestas en la caché.

### Arquitectura del Proyecto:

- **Redis:** Se configuran múltiples instancias de Redis (hasta 4 particiones).
- **gRPC:** Se usa para las comunicaciones entre el servidor y el cliente para resolver consultas DNS.
- **Flask:** Proporciona una API REST que maneja las consultas de DNS y utiliza Redis como almacenamiento en caché.
- **Particionado Hash:** La distribución de datos se realiza utilizando una función hash para distribuir las consultas entre las instancias de Redis.

## Requisitos

- Docker
- Docker Compose

### Librerías Usadas:

- `Flask`: Para la API.
- `redis-py`: Para la conexión con Redis.
- `grpcio`: Para la implementación de gRPC.
- `pandas`: Para leer y manejar los datos CSV.
- `requests`: Para hacer solicitudes HTTP a la API.

## Instalación

1. **Clonar el Repositorio:**

   ```bash
   git clone <URL del repositorio>
   cd <directorio del proyecto>
2. **Estructura del proyecto:**
   ```bash
   ├── api/
   │   ├── app.py  # Código principal de la API
   ├── grpc_server/
   │   ├── grpc_server.py  # Código principal del servidor gRPC
   ├── docker-compose.yml  # Definición de servicios de Docker
   ├── README.md  # Instrucciones del proyecto
3. **Configuración de Redis y gRPC**
 en Docker Compose Este proyecto utiliza múltiples instancias de Redis. Para configurar y ejecutar las instancias con gRPC, asegúrate de tener Docker Compose instalado.
4.**Ejecutar el proyecto:**
   ```bash
   docker-compose up --build
5.**politicas de remocion**
Puedes configurar la política de remoción en Redis directamente utilizando los comandos de Redis o configurando el archivo redis.conf para definir cómo se eliminan las claves cuando Redis alcanza el límite de memoria

**Observaciones**
Asegúrate de que todos los contenedores estén corriendo correctamente antes de realizar consultas a la API.


   

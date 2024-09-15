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

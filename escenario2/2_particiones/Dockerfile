# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . /app
COPY cache_pb2.py /app/
COPY cache_pb2_grpc.py /app/

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del gRPC
EXPOSE 50051

# Comando para ejecutar el servidor gRPC
CMD ["python", "grpc_server.py"]

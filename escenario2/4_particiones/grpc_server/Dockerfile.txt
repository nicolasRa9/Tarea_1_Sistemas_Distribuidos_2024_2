# Usa una imagen de Python slim como base
FROM python:3.9-slim

WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos
COPY . .

# Ejecuta el servidor gRPC
CMD ["python", "grpc_server.py"]

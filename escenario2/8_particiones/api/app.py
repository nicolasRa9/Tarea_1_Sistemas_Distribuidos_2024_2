import hashlib
from flask import Flask, request, jsonify
import redis
import grpc_client  # El archivo del cliente gRPC

app = Flask(__name__)

# Conexión a Redis
redis_clients = [
    redis.StrictRedis(host='redis1', port=6379, db=0),
    redis.StrictRedis(host='redis2', port=6379, db=0),
    redis.StrictRedis(host='redis3', port=6379, db=0),
    redis.StrictRedis(host='redis4', port=6379, db=0),
    redis.StrictRedis(host='redis5', port=6379, db=0),
    redis.StrictRedis(host='redis6', port=6379, db=0),
    redis.StrictRedis(host='redis7', port=6379, db=0),
    redis.StrictRedis(host='redis8', port=6379, db=0)
]

def get_redis_instance(domain):
    """Usa el hash del dominio para seleccionar una instancia de Redis"""
    hash_value = int(hashlib.md5(domain.encode()).hexdigest(), 16)
    return redis_clients[hash_value % len(redis_clients)]

@app.route('/resolve', methods=['POST'])
def resolve_domain():
    data = request.json
    domain = data.get('domain')

    if not domain:
        return jsonify({'error': 'No domain provided'}), 400

    # Seleccionar la instancia de Redis en función del hash del dominio
    redis_instance = get_redis_instance(domain)

    # Verificar si el dominio está en la caché
    cached_ip = redis_instance.hget('dns_cache', domain)
    if cached_ip:
        return jsonify({'domain': domain, 'ip': cached_ip.decode('utf-8'), 'source': 'cache'}), 200

    # Si no está en la caché, llamar a gRPC
    resolved_ip = grpc_client.get_dns_resolution(domain)

    # Guardar el resultado en Redis (en la instancia seleccionada)
    redis_instance.hset('dns_cache', domain, resolved_ip)

    return jsonify({'domain': domain, 'ip': resolved_ip, 'source': 'grpc'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import redis
import grpc_client  # El archivo del cliente gRPC

app = Flask(__name__)

# Conectar a una sola instancia de Redis
redis_instance = redis.StrictRedis(host='redis1', port=6379, db=0)

@app.route('/resolve', methods=['POST'])
def resolve_domain():
    data = request.json
    domain = data.get('domain')

    if not domain:
        return jsonify({'error': 'No domain provided'}), 400

    # Verificar si el dominio está en la caché
    cached_ip = redis_instance.hget('dns_cache', domain)
    if cached_ip:
        return jsonify({'domain': domain, 'ip': cached_ip.decode('utf-8'), 'source': 'cache'}), 200

    # Si no está en la caché, llamar a gRPC para resolver el dominio
    resolved_ip = grpc_client.get_dns_resolution(domain)

    # Guardar el resultado en Redis
    redis_instance.hset('dns_cache', domain, resolved_ip)

    return jsonify({'domain': domain, 'ip': resolved_ip, 'source': 'grpc'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

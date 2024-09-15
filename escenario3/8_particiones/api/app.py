import hashlib
from flask import Flask, request, jsonify
import redis
import grpc_client  # El archivo del cliente gRPC

app = Flask(__name__)

# Conectar a las 4 instancias de Redis
redis_clients = [
    redis.StrictRedis(host='redis1', port=6379, db=0),  # Primera instancia Redis
    redis.StrictRedis(host='redis2', port=6379, db=0),  # Segunda instancia Redis
    redis.StrictRedis(host='redis3', port=6379, db=0),  # Tercera instancia Redis
    redis.StrictRedis(host='redis4', port=6379, db=0),
    redis.StrictRedis(host='redis5', port=6379, db=0),  # Primera instancia Redis
    redis.StrictRedis(host='redis6', port=6379, db=0),  # Segunda instancia Redis
    redis.StrictRedis(host='redis7', port=6379, db=0),  # Tercera instancia Redis
    redis.StrictRedis(host='redis8', port=6379, db=0)
                                                   
]

# Definir las reglas de partición
partition_map = {
    'A-G': redis_clients[0],
    'H-N': redis_clients[1],
    'O-T': redis_clients[2],
    'U-Z': redis_clients[3]
}

def get_redis_instance(domain):
    """Función que selecciona una partición (Redis) en función del dominio"""
    first_char = domain[0].upper()
    
    if 'A' <= first_char <= 'G':
        return partition_map['A-G']
    elif 'H' <= first_char <= 'N':
        return partition_map['H-N']
    elif 'O' <= first_char <= 'T':
        return partition_map['O-T']
    elif 'U' <= first_char <= 'Z':
        return partition_map['U-Z']
    else:
        # Si el dominio comienza con un carácter no alfabético
        return partition_map['A-G']  # Puedes ajustar esta lógica si lo necesitas

@app.route('/resolve', methods=['POST'])
def resolve_domain():
    data = request.json
    domain = data.get('domain')

    if not domain:
        return jsonify({'error': 'No domain provided'}), 400

    # Seleccionar la instancia de Redis basada en la partición
    redis_instance = get_redis_instance(domain)

    # Verificar si el dominio está en la caché
    cached_ip = redis_instance.hget('dns_cache', domain)
    if cached_ip:
        return jsonify({'domain': domain, 'ip': cached_ip.decode('utf-8'), 'source': 'cache'}), 200

    # Si no está en la caché, llamar a gRPC para resolver el dominio
    resolved_ip = grpc_client.get_dns_resolution(domain)

    # Guardar el resultado en Redis (en la partición seleccionada)
    redis_instance.hset('dns_cache', domain, resolved_ip)

    return jsonify({'domain': domain, 'ip': resolved_ip, 'source': 'grpc'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

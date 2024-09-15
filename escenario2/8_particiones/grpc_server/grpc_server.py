import grpc
from concurrent import futures
import cache_pb2
import cache_pb2_grpc
import redis
import hashlib

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

class DNSResolverServicer(cache_pb2_grpc.DNSResolverServicer):
    def Resolve(self, request, context):
        domain = request.domain

        redis_instance = get_redis_instance(domain)
        cached_ip = redis_instance.hget('dns_cache', domain)

        if cached_ip:
            return cache_pb2.ResolveReply(ip=cached_ip.decode('utf-8'), source='cache')

        # Simular resolución DNS (aquí deberías integrar la lógica real o usar un servicio DNS real)
        resolved_ip = "8.8.8.8"  # Simulación de IP

        redis_instance.hset('dns_cache', domain, resolved_ip)
        return cache_pb2.ResolveReply(ip=resolved_ip, source='grpc')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_pb2_grpc.add_DNSResolverServicer_to_server(DNSResolverServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

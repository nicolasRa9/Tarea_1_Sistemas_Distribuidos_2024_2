import redis
from concurrent import futures
import grpc
import cache_pb2
import cache_pb2_grpc

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

class CacheServiceServicer(cache_pb2_grpc.CacheServiceServicer):
    def GetValue(self, request, context):
        key = request.key
        value = r.get(key)
        if value:
            return cache_pb2.ValueResponse(value=value.decode('utf-8'), found=True)
        else:
            return cache_pb2.ValueResponse(value="", found=False)

    def SetValue(self, request, context):
        key = request.key
        value = request.value
        r.set(key, value)
        return cache_pb2.SetResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_pb2_grpc.add_CacheServiceServicer_to_server(CacheServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051 con Redis")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

import grpc
import cache_pb2
import cache_pb2_grpc

def get_dns_resolution(domain):
    with grpc.insecure_channel('grpc_server:50051') as channel:
        stub = cache_pb2_grpc.DNSResolverStub(channel)
        response = stub.Resolve(cache_pb2.ResolveRequest(domain=domain))
    return response.ip

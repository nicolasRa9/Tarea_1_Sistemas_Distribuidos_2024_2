import grpc
import cache_pb2
import cache_pb2_grpc
import pandas as pd
import hashlib
import redis
import dns.resolver  # Para las consultas DNS

# Configuración de 2 instancias de Redis
redis_servers = {
    0: redis.Redis(host='localhost', port=6379),
    1: redis.Redis(host='localhost', port=6380)
}

def get_redis_instance(key):
    """Esta función toma una clave, calcula su hash y devuelve la instancia de Redis adecuada."""
    hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
    # Utilizamos % 2 porque tenemos 2 particiones (dos servidores Redis)
    return redis_servers[hash_value % 2]

def perform_dns_query(domain):
    """Realiza una consulta DNS real para obtener la dirección IP del dominio."""
    try:
        # Realiza una consulta DNS tipo A para obtener la dirección IP
        answer = dns.resolver.resolve(domain, 'A')
        ip_address = answer[0].to_text()  # Obtenemos la primera respuesta
        return ip_address
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return None
    except dns.exception.Timeout:
        return None
    except Exception as e:
        print(f"Error resolviendo {domain}: {e}")
        return None

def run():
    # Establecer la conexión con el servidor gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = cache_pb2_grpc.CacheServiceStub(channel)
        
        # Leer el dataset (CSV) con pandas y limitar a las primeras 10,000 filas
        dataset = pd.read_csv("C:\\Users\\Nicolas\\Documents\\Sistema_distribuido\\Tarea1\\Data\\domains.csv").head(20000)
        dataset.columns = ['domain']
        # Imprimir los nombres de las columnas para verificar
        print("Columnas del dataset:", dataset.columns)
        
        for index, row in dataset.iterrows():
            domain = row['domain']  # Asegúrate de que 'domain' es el nombre correcto

            # Obtén la instancia de Redis basada en la clave (dominio)
            redis_instance = get_redis_instance(domain)
            
            # Primero intenta obtener el valor de Redis
            cached_value = redis_instance.get(domain)
            if cached_value:
                print(f"Cache HIT para {domain}: {cached_value.decode('utf-8')}")
            else:
                print(f"Cache MISS para {domain}. Realizando consulta DNS real...")

                # Realiza la consulta DNS real usando dnspython
                ip_address = perform_dns_query(domain)

                if ip_address:
                    print(f"Dominio: {domain}, IP obtenida: {ip_address}")
                    
                    # Almacena el valor en la instancia de Redis correspondiente
                    redis_instance.set(domain, ip_address)
                else:
                    print(f"No se pudo obtener la IP para el dominio {domain}.")
                    # Almacenar un valor nulo o no almacenar dependiendo de la lógica

if __name__ == '__main__':
    run()

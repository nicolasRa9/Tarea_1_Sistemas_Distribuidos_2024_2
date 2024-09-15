import redis
import dns.resolver
import random
import pandas as pd

# Cargar el dataset sin encabezado
dataset = pd.read_csv(r'C:\Users\Nicolas\Documents\Sistema_distribuido\Tarea1\Data\domains.csv', header=None)

# Asignar un nombre a la columna
dataset.columns = ['domain']
# Limitar el dataset a 1000 dominios para las pruebas
limited_dataset = dataset['domain'].head(1000)

# Simular consultas DNS usando los dominios


# Verificar los primeros registros
print(dataset.head())
# Conectar a Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

# Función para consultar DNS y cachear los resultados
def resolve_domain(domain):
    # Revisar si el dominio está en caché
    cached_ip = cache.get(domain)
    if cached_ip:
        print(f"Cache HIT para {domain}: {cached_ip.decode('utf-8')}")
        return cached_ip.decode('utf-8')
    else:
        print(f"Cache MISS para {domain}. Realizando consulta DNS...")
        try:
            # Realiza la consulta DNS
            result = dns.resolver.resolve(domain, 'A')
            ip = result[0].to_text()

            # Guardar el resultado en el caché con expiración de 1 hora
            cache.set(domain, ip, ex=3600)
            return ip
        except dns.resolver.NXDOMAIN:
            print(f"Dominio {domain} no encontrado.")
            return None
        except Exception as e:
            print(f"Error resolviendo {domain}: {str(e)}")
            return None
# Simular consultas DNS usando el dataset
# Suponemos que el dataset tiene una columna llamada 'domain' con los nombres de dominio

# Limitar el dataset a 1000 dominios para las pruebas
limited_dataset = dataset['domain'].head(1000)

for domain in limited_dataset:
    resolve_domain(domain)


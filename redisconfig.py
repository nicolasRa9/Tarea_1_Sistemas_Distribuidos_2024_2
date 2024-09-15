import dns.resolver

def resolve_domain(domain):
    # Primero revisamos si el dominio ya está en el caché
    cached_ip = cache.get(domain)

    if cached_ip:
        print(f"Cache HIT para {domain}: {cached_ip.decode('utf-8')}")
        return cached_ip.decode('utf-8')
    else:
        print(f"Cache MISS para {domain}. Realizando consulta DNS...")
        try:
            # Realiza la consulta DNS (sin usar caché del sistema)
            result = dns.resolver.resolve(domain, 'A')
            ip = result[0].to_text()

            # Almacenar el resultado en Redis (con TTL de 1 hora)
            cache.set(domain, ip, ex=3600)  # ex=3600 indica 1 hora de expiración

            return ip
        except dns.resolver.NXDOMAIN:
            print(f"Dominio {domain} no encontrado.")
            return None
        except Exception as e:
            print(f"Error resolviendo {domain}: {str(e)}")
            return None

# Tarea_1_Sistemas_Distribuidos_2024_2
Primero, definimos el servicio gRPC en un archivo .proto. Este archivo describe las llamadas remotas que el cliente gRPC puede hacer y los datos que intercambia con el servidor.
Este archivo define dos métodos:
GetValue: para obtener un valor de Redis usando una clave.
SetValue: para guardar un valor en Redis con una clave.
Una vez que tengas tu archivo .proto, genera los archivos necesarios para Python utilizando el compilador protoc.
Esto generará los archivos cache_pb2.py y cache_pb2_grpc.py, que puedes usar para construir el servidor y el cliente gRPC.
Ahora, implementamos el servidor gRPC que manejará las peticiones y se comunicará con Redis. Aquí conectamos el servidor gRPC a múltiples instancias de Redis.
Este servidor gRPC:
* Se conecta a varias instancias de Redis.
* Usa una función hash para decidir en qué partición (instancia Redis) guardar/recuperar los datos.
* Expone los métodos GetValue y SetValue a través de gRPC.
El cliente gRPC se comunica con el servidor gRPC para obtener y guardar datos en Redis.

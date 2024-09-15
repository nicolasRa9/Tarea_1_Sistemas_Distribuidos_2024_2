import requests
import pandas as pd
import time

# Ruta al archivo CSV que contiene los dominios
csv_file_path = 'C:/Users/Nicolas/Documents/Sistema_distribuido/Tarea1/Data/domains.csv'

# Cargar el CSV, sin nombres de columna
# El parámetro `header=None` indica que no hay nombres de columna
# Limita a 10,000 filas con `nrows=10000`
df = pd.read_csv(csv_file_path, header=None, nrows=10000)

# URL de la API (modifícala si es necesario)
url = 'http://localhost:5000/resolve'

# Medir el tiempo de todas las consultas
start_time = time.time()

# Realizar las consultas a la API
for index, row in df.iterrows():
    dominio = row[0]  # La primera (y única) columna contiene los dominios
    payload = {'domain': dominio}
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Dominio: {data['domain']}, IP: {data['ip']}, Origen: {data['source']}")
        else:
            print(f"Error al consultar el dominio {dominio}: {response.status_code}")
    except Exception as e:
        print(f"Error al procesar el dominio {dominio}: {e}")

# Medir el tiempo final
end_time = time.time()

# Calcular el tiempo total en segundos
total_time = end_time - start_time

print(f"Tiempo total para realizar todas las consultas: {total_time:.2f} segundos")

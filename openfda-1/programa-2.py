import http.client
import json

#Nombre del servidor
server_name = "api.fda.gov"
resource = "/drug/label.json"

conection = http.client.HTTPSConnection(server_name)

#Especifico el cabecero en concreto
headers = {'User-Agent': 'http-client'}
#Igualo el limite a 10, para que no me salgan mas de 10 medicamentos
limit="?limit=10"

#Enviamos una peticion al servidor para establecer la conexion
conection.request("GET", resource + limit , None, headers)

response = conection.getresponse()
medicines= response.read().decode("utf-8")
conection.close()

#Leemos el contenido json
medicines_json=json.loads(medicines)
drugs=medicines_json['results']

#Imprimo los id's de los medicamentos
print(" Consulta de 10 identificadores de medicamentos ")

for medicines in drugs:
    print("ID: ",medicines['id'])


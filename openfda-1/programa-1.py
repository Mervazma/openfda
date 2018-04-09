import http.client
import json

#Nombre del servidor
server_name = "api.fda.gov"
resource = "/drug/label.json"

conection = http.client.HTTPSConnection(server_name)

#Especifico el cabecero en concreto
headers = {'User-Agent': 'http-client'}

#Enviamos una peticion al servidor para establecer la conexion
conection.request("GET", resource, None, headers)

response = conection.getresponse()
medicines = response.read().decode("utf-8")
conection.close()

#Leemos el contenido json
medicines_json=json.loads(medicines)
meta=medicines_json['meta']
drugs=medicines_json['results'][0]

#Imprimo el id, nombre y fabricante del producto
id=drugs['id']
print("ID:\n",id)
print("")

purpose=drugs['purpose'][0]
print("Proposito del producto:\n",purpose)
print("")

name=drugs['openfda']['manufacturer_name'][0]
print("Nombre del fabricante del producto:\n",name)
print("")


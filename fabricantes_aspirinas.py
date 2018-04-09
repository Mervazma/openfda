import http.client
import json

#Nombre del servidor
server_name = "api.fda.gov"
resource = "/drug/label.json"
skip=0

conection = http.client.HTTPSConnection(server_name)

query = "/?search=active_ingredient:acetylsalicylic&limit=100&skip="

#Especifico el cabecero en concreto
headers = {'User-Agent': 'http-client'}

#Enviamos una peticion al servidor para establecer la conexion
conection.request("GET", resource + query +str(skip), None, headers)

response = conection.getresponse()
aspirin= response.read().decode("utf-8")

conection.close()
#Leo el contenido json
aspirins = json.loads(aspirin)['results']

print("\nNOMBRES Y ID'S DE TODOS LOS FABRICANTES QUE PRODUCEN ASPIRINAS:\n")

#Imprimo los fabricantes de aspirinas
for aspirin in aspirins:

    if aspirin['openfda']:
        manufacturer = aspirin['openfda']['manufacturer_name'][0]
        print("- Fabricante: " ,manufacturer)
    else:
        print("- Fabricante no disponible")

    print("  ID: ", aspirin['id'])

if (len(aspirin))==100:
    skip= skip + 100
import http.client
import json

#Nombre del servidor
server_name = "api.fda.gov"
resource = "/drug/label.json"

conection = http.client.HTTPSConnection(server_name)

limit= "?limit=10"

#Especifico el cabecero en concreto
headers = {'User-Agent': 'http-client'}

#Enviamos una peticion al servidor para establecer la conexion
conection.request("GET", resource + limit, None, headers)


response = conection.getresponse()
medicines = response.read().decode("utf-8")
conection.close()

medicines_json = json.loads(medicines)
drugs = medicines_json['results']

#Lo creo vacio para introducirle la siguiente informacion dentro de clientinfo
clientinfo = ""

for medicines in drugs:
    openfda = medicines['openfda']
    if openfda:
        brand_name = openfda['brand_name']
        brand_name = ','.join(brand_name)
        #Imprime la marca del medicamento

        substance_name = openfda['substance_name']
        substance_name = ','.join(substance_name)
        #Imprime el nombre del medicamento

        clientinfo = clientinfo + brand_name + "\t" + substance_name + "\n"
    else:
        no_info = ("Informacion no disponible\n")
        clientinfo = clientinfo + no_info

#Creamos el servidor
import socket

IP = "127.0.0.1"
PORT = 9654
MAX_OPEN_REQUEST = 5

#Funcion que atiende al cliente y le envia un mensaje de respuesta en contenido HTTML
def infoforclient(clientsocket):

    # En este contenido pondremos el texto en HTML que queremos que se visualice en el navegador cliente
    contenido = """
    <html>
    <h1>Brand name Substance name</h1>
    <pre> """ + clientinfo + """
    </pre>
    </html>
    """

    # Creamos el mensaje de respuesta. Tiene que ser un mensaje en HTTP
    linea_inicial = "HTTP/1.1 200 OK\n" #Indicamos que todo esta bien
    headers = "Content-Type: text/html\n"
    headers += "Content-Length: {}\n".format(len(str.encode(contenido)))
    #creamos el mensaje que se mostrara en el navegador cliente
    mensaje_respuesta = str.encode(linea_inicial + headers + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()

#Creo un socket para el servidor
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Asociamos el socket a la direccion IP y a los puertos del servidor
try:

    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUEST)

    #Imprimimos el mensaje de esperando clientes y peticion recibida como hacen todos los servidores
    while True:

        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()


        print("  Peticion de cliente recibida. IP: {}".format(address))
        infoforclient(clientsocket)

except socket.error: #En el caso de que repitamos el puerto
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")

    clientsocket.close()
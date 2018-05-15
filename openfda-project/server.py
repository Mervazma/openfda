import http.server
import http.client
import socketserver
import json

#Puerto donde lanzar el servidor
puerto = 8000


#Nombre del servidor
server_name = "api.fda.gov"
resource = "/drug/label.json"


#Especifico el cabecero en concreto
headers = {'User-Agent': 'http-client'}


#Clase con nuestro manejador.
class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    #creo una fucion para obtener informacion de la pagina
    def connection_req(self, limit=10, search_str= "" ):
        # establezco la conexion, contiene la info de la pag web
        connection = http.client.HTTPSConnection(server_name)
        # Enviamos una peticion al servidor para establecer la conexion
        connection.request("GET", resource + "?limit="+str(limit), None, headers)
        print(resource + "?limit="+str(limit))
        response = connection.getresponse()
        medicines = response.read().decode("utf-8")
        medicines_json = json.loads(medicines)

        #cadena con la peticion
        request = "{}?limit={}".format(resource, limit)

        #Si hay parametros, los añade a la peticion para acceder a la informacion
        if search_str != "":
            request += "&{}".format(search_str)
            print("Recurso solicitado: {}".format(request))
            print("  * {} {}".format(response.status, response.reason))


        connection.close()
        return medicines_json
    #creo una funcion para luego poder llamarla para abrir la pagina principal
    def index_req(self):

        html = """
                   <html>
                       <head>
                           <title></title>
                       </head>
                       <body style="background-color:lightgreen;">
                           <h1>GESTION DE FARMACOS Y EMPRESAS</h1>
                           <h2>MENU PRINCIPAL:</h2>
                           <form method="get" action="listDrugs">
                               <input type = "submit" value="LISTA DE FARMACOS">
                               </input>
                           </form>
                           ----------------------------------------------------------
                           <form method="get" action="searchDrug">
                               <input type = "submit" value="BUSCAR MEDICAMENTOS">
                               <input type = "text" name="drug"></input>
                               </input>
                           </form>
                           ----------------------------------------------------------
                           <form method="get" action="listCompanies">
                               <input type = "submit" value="LISTA DE EMPRESAS">
                               </input>
                           </form>
                           ----------------------------------------------------------
                           <form method="get" action="searchCompany">
                               <input type = "submit" value="BUSCAR EMPRESAS">
                               <input type = "text" name="company"></input>
                               </input>
                           </form>
                           ----------------------------------------------------------
                            <form method="get" action="listWarnings">
                        <input type = "submit" value="LISTA DE ADVERTENCIAS">

                        </input>

                    </form>
                        
                       
                       </body>
                   </html>
                       """

        return html

    #creo una funcion con la lista de los farmacos
    def listdrugs_req(self, limit=10 ):

        medicines_html = (' <!DOCTYPE html>\n'
                     '<html lang="es">\n'
                     '<head>\n'
                     '    <meta charset="UTF-8">\n'
                     '</head>\n'
                     '<body style="background-color:lightgreen;">\n'
                     '<p>Listado de fármacos : </p>'
                     '\n'
                     '<ul>\n')



        drugs = self.connection_req(limit)
        drug = drugs["results"]

        for i in range(len(drug)):

            if drug[i]["openfda"]:
                substance_name = drug[i]["openfda"]["generic_name"][0]
                medicines_html += '<ul><li>' + substance_name  + '</li></ul>'


        return medicines_html


    #creo una funcion con la lista de las empresas
    def listcompanies_req(self, limit=10):

        fabricantes_html = (' <!DOCTYPE html>\n'
                     '<html lang="es">\n'
                     '<head>\n'
                     '    <meta charset="UTF-8">\n'
                     '</head>\n'
                     '<body style="background-color:lightgreen;">\n'
                     '<p>Fabricantes</p>'
                     '\n'
                     '<ul>\n')

        companies = self.connection_req(limit)
        company = companies["results"]

        for i in range(len(company)):

            if company[i]["openfda"]:
                manufacturer_name = company[i]["openfda"]["manufacturer_name"][0]
                fabricantes_html += '<ul><li>' + manufacturer_name + '</li></ul>'


        return fabricantes_html

    #creo una funcion con la lista de las advertencias
    def listwarnings_req(self, limit):  # Crea el html con el identificador del medicamento y sus advertencias.

        info = self.connection_req(limit)
        warning = info['results']

        warnings_html = (' <!DOCTYPE html>\n'
                     '<html lang="es">\n'
                     '<head>\n'
                     '    <meta charset="UTF-8">\n'
                     '</head>\n'
                     '<body style="background-color:lightgreen;">\n'
                     '<p>Lista de advertencias:</p>'
                     '\n'
                     '<ul>\n')

        for i in range(len(warning)):
            id = warning[i]["id"]  # Identificador

            if "warnings" in warning[i].keys():
                datos = warning[i]['warnings'][0]  # Advertencias
                warnings_html+= '<ul><li>' + datos + '</li></ul>'


        return warnings_html

    #creo una funcion que recibe la informacion que busco de farmacos y empresas
    def web_req(self,list):

        list_html = """<html>
                            <head> 
                                <title>OpenFDA</title> 
                            </head>
                            <body style="background-color: lightgreen"> 
                                <ul>"""
        for e in list:
            list_html += "<ul><li>" + e + "</li></ul>"+"<br>"
        list_html += "</body></html>"
        return list_html


    def do_GET(self):

        recurso_list = self.path.split("?")


        if len(recurso_list) > 1:
            parameters = recurso_list[1]
        else:
            parameters = ""


        limit = 10


        #Obtener los parametros
        if parameters:
            print("Hay parametros")
            parse_limit = parameters.split("=")
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("NO HAY PARAMETROS")


        #Menu principal
        if self.path == '/':
            html= self.index_req()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(html, "utf8"))

        #Listado de medicamentos
        elif 'listDrugs' in self.path:
            print("Listado de farmacos solicitado:")
            message = self.listdrugs_req(limit)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))

        #Listado de empresas
        elif 'listCompanies' in self.path:
            print("Listado de empresas solicitado: ")
            message = self.listcompanies_req(limit)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))

        #Para buscar farmacos especificos
        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            drug = self.path.split('=')[1]

            drugs = []
            connection = http.client.HTTPSConnection(server_name)
            connection.request("GET", resource + "?limit=" + str(limit) + "&search=active_ingredient:" + drug)
            response = connection.getresponse()
            datos = response.read().decode("utf8")
            info = json.loads(datos)
            info_drugs = info['results']
            for item in info_drugs:
                if ('generic_name' in item['openfda']):
                    drugs.append(item['openfda']['generic_name'][0])
                else:
                    drugs.append('El nombre del farmaco no existe')
            pagina_html = self.web_req(drugs)
            self.wfile.write(bytes(pagina_html, "utf8"))


        #Para buscar empresas especificas
        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            limit = 10
            company=self.path.split('=')[1]
            companies = []

            connection = http.client.HTTPSConnection(server_name)
            connection.request("GET", resource + "?limit=" + str(limit) + '&search=openfda.manufacturer_name:' + company)
            response = connection.getresponse()
            datos = response.read().decode("utf8")
            info = json.loads(datos)
            info_companies = info['results']

            for item in info_companies:
                if ('manufacturer_name' in item['openfda']):
                    companies.append(item['openfda']['manufacturer_name'][0])
                else:
                    companies.append('El nombre de la empresa no existe')
            pagina_html = self.web_req(companies)
            self.wfile.write(bytes(pagina_html, "utf8"))


        #Listado de advertencias
        elif 'listWarnings' in self.path:
            mensaje=self.listwarnings_req(limit)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif 'redirect' in self.path:
            print("Redirigimos la dirección a la página principal")
            self.send_response(301)
            self.send_header('Location', 'http://localhost:' + str(puerto))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())

        return

#Servidor
#Para poder utlizar siempre el mismo puerto
socketserver.TCPServer.allow_reuse_address = True
Handler = TestHTTPRequestHandler

#manda a tu manejador de peticiones que atienda y responda la peticion
httpd = socketserver.TCPServer(("", puerto), Handler)

print("SIRVIENDO EN EL PUERTO: ", puerto)

try:

    httpd.serve_forever()

except KeyboardInterrupt:
    pass
httpd.server_close()
print("")
print("Servidor parado")
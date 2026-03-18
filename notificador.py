import http.server, socketserver, json, smtplib, random, os
from email.message import EmailMessage

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))
            codigo = str(random.randint(100000, 999999))
            
            remitente = "elisgarces1966@gmail.com"
            password = "dcrj jzya cuar ncvm" 
            
            msg = EmailMessage()
            msg['Subject'] = f'Codigo U-KEY: {codigo}'
            msg['From'] = remitente
            msg['To'] = data['email']
            msg.set_content(f"Hola {data['nombre']}, tu codigo es: {codigo}")

            print(f"INTENTO: Enviando desde {remitente} a {data['email']}...")

            # USAMOS PUERTO 587 QUE ES MÁS COMPATIBLE CON RENDER
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls() 
            server.login(remitente, password)
            server.send_message(msg)
            server.quit()
            
            print("¡EXITO TOTAL!")
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
            
        except Exception as e:
            # ESTO ES LO QUE NECESITO LEER EN LOS LOGS
            print(f"DIAGNOSTICO_GMAIL: {str(e)}")
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

puerto = int(os.environ.get("PORT", 10000))
httpd = ThreadingHTTPServer(("", puerto), MyHandler)
httpd.serve_forever()

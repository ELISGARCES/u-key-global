import http.server, socketserver, json, smtplib, random, os
from email.message import EmailMessage

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/enviar_verificacion':
            try:
                content_length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(content_length))
                codigo = str(random.randint(100000, 999999))
                
                remitente = "elisgarces1966@gmail.com"
                password = "xkvm xqgd pobn soei"
                
                msg = EmailMessage()
                msg['Subject'] = f'Tu Codigo U-KEY: {codigo}'
                msg['From'] = remitente
                msg['To'] = data['email']
                msg.set_content(f"Hola {data['nombre']},\n\nTu codigo de verificacion es: {codigo}\n\nU-KEY System.")

                # CAMBIO A PUERTO 587 (MÁS COMPATIBLE CON RENDER)
                print(f"--- INICIANDO ENVIO A {data['email']} ---")
                server = smtplib.SMTP('smtp.gmail.com', 587, timeout=20)
                server.starttls() # Inicia el tunel seguro
                server.login(remitente, password)
                server.send_message(msg)
                server.quit()
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
                print(f"--- EXITO TOTAL: {codigo} ENVIADO ---")

            except Exception as e:
                # ESTO FORZARÁ EL ERROR EN EL LOG PARA QUE LO VEAMOS
                print(f"!!! ERROR DETECTADO: {str(e)} !!!")
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())

class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

puerto = int(os.environ.get("PORT", 10000))
httpd = ReusableTCPServer(("", puerto), MyHandler)
print(f"Servidor U-KEY escuchando en puerto {puerto}")
httpd.serve_forever()

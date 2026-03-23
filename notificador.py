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
                password = "xkvm xqgd pobn soei" # Tu nueva llave de ayer
                
                msg = EmailMessage()
                msg['Subject'] = f'Codigo U-KEY: {codigo}'
                msg['From'] = remitente
                msg['To'] = data['email']
                msg.set_content(f"Hola {data['nombre']},\n\nTu codigo es: {codigo}")

                # INTENTO DE CONEXIÓN CON REINTENTO
                print(f"Intentando enviar correo a {data['email']}...")
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15) as smtp:
                    smtp.login(remitente, password)
                    smtp.send_message(msg)
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
                print(f"ÉXITO TOTAL: {codigo}")

            except Exception as e:
                error_msg = str(e)
                print(f"DIAGNÓSTICO: {error_msg}")
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                # Esto enviará el error real a tu celular para que lo leamos
                self.wfile.write(json.dumps({"error": error_msg}).encode())

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

puerto = int(os.environ.get("PORT", 10000))
with ReusableTCPServer(("", puerto), MyHandler) as httpd:
    print(f"Servidor U-KEY operativo en puerto {puerto}")
    httpd.serve_forever()

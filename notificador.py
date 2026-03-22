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
                
                msg = EmailMessage()
                msg['Subject'] = f'Tu Codigo U-KEY: {codigo}'
                msg['From'] = "elisgarces1966@gmail.com"
                msg['To'] = data['email']
                msg.set_content(f"Hola {data['nombre']},\n\nTu código de verificación global es: {codigo}\n\nU-KEY System.")

                # Conexión reforzada con Gmail
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("elisgarces1966@gmail.com", "dcrj jzya cuar ncvm")
                    smtp.send_message(msg)
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
                print(f"Código enviado con éxito a {data['email']}")

            except Exception as e:
                print(f"ERROR CRÍTICO: {str(e)}")
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())

# Forzar puerto de Render
puerto = int(os.environ.get("PORT", 10000))
with socketserver.TCPServer(("", puerto), MyHandler) as httpd:
    print(f"Servidor U-KEY operativo en puerto {puerto}")
    httpd.serve_forever()

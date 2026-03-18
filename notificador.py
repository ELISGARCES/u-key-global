import http.server
import socketserver
import json
import smtplib
import random
import os
from email.message import EmailMessage

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
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            codigo = str(random.randint(100000, 999999))
            
            remitente = "elisgarces1966@gmail.com"
            # Asegúrate de que esta clave de 16 letras no tenga espacios extra
            password = "yyuy yugv tjbh fkms"
            
            msg = EmailMessage()
            msg['Subject'] = f'Codigo U-KEY: {codigo}'
            msg['From'] = remitente
            msg['To'] = data['email']
            msg.set_content(f"Hola {data['nombre']},\n\nTu codigo es: {codigo}")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(remitente, password)
                smtp.send_message(msg)
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
            
        except Exception as e:
            print(f"ERROR_LOG: {e}")
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

# Cambiamos el puerto por defecto a 10000 para Render
puerto = int(os.environ.get("PORT", 10000))
with socketserver.TCPServer(("", puerto), MyHandler) as httpd:
    print(f"Servidor activo en puerto {puerto}")
    httpd.serve_forever()

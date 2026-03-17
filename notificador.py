import http.server
import socketserver
import json
import smtplib
import random
import os
from email.message import EmailMessage

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # ESTO ES LO QUE FALTA: Los permisos para que Render acepte a GitHub
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        codigo = str(random.randint(100000, 999999))
        
        # USA TU CORREO Y TU CLAVE DE 16 LETRAS
        remitente = "elisgarces1966@gmail.com" 
        password = "yyuy yugv tjbh fkms" 
        
        msg = EmailMessage()
        msg['Subject'] = f'Tu Código U-KEY: {codigo}'
        msg['From'] = remitente
        msg['To'] = data['email']
        msg.set_content(f"Hola {data['nombre']},\n\nTu código de acceso seguro a U-KEY es: {codigo}")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(remitente, password)
                smtp.send_message(msg)
            
            self.send_response(200)
            # PERMISOS TAMBIÉN AQUÍ
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            print(f"Error: {e}")

puerto = int(os.environ.get("PORT", 8080))
with socketserver.TCPServer(("", puerto), MyHandler) as httpd:
    print(f"Servidor U-KEY Activo en Puerto {puerto}")
    httpd.serve_forever()

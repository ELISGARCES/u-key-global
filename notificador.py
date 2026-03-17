import http.server
import socketserver
import json
import smtplib
import random
import os  # <-- Esto es nuevo para Render
from email.message import EmailMessage

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
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
        
        # COLOCA TUS DATOS AQUÍ DE NUEVO (CON COMILLAS)
        remitente = "elisgarces1966@gmail.com" 
        password = "tu_clave_de_16_letras_aqui"
        
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
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
        except Exception:
            self.send_response(500)
            self.end_headers()

# Esta línea es la que permite que Render funcione correctamente
puerto = int(os.environ.get("PORT", 8080))
with socketserver.TCPServer(("", puerto), MyHandler) as httpd:
    print(f"Servidor U-KEY Activo en Puerto {puerto}")
    httpd.serve_forever()

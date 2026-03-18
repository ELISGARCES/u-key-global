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
            
            # --- DATOS CRITICOS ---
            remitente = "elisgarces1966@gmail.com"
            password = "yyuy yugv tjbh fkms"
            # ----------------------
            
            msg = EmailMessage()
            msg['Subject'] = f'Codigo U-KEY: {codigo}'
            msg['From'] = remitente
            msg['To'] = data['email']
            msg.set_content(f"Hola {data['nombre']},\n\nTu codigo es: {codigo}")

            print(f"DEBUG: Intentando enviar correo a {data['email']}")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(remitente, password)
                smtp.send_message(msg)
            
            print("DEBUG: ¡CORREO ENVIADO!")
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
            
        except Exception as e:
            # ESTA LINEA ES LA QUE NECESITO SI FALLA
            print(f"FALLO_SISTEMA: {str(e)}")
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

puerto = int(os.environ.get("PORT", 10000))
with socketserver.TCPServer(("", puerto), MyHandler) as httpd:
    print(f"Servidor en puerto {puerto}")
    httpd.serve_forever()

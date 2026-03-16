import http.server
import socketserver
import json
import smtplib
import random
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
        
        # Generar código de 6 dígitos
        codigo = str(random.randint(100000, 999999))
        
        # CONFIGURA AQUÍ TU GMAIL
        remitente = "elisgarces1966@gmail.com"
        password = "yyuy yugv tjbh fkms"


        
        msg = EmailMessage()
        msg['Subject'] = f'Tu Código U-KEY: {codigo}'
        msg['From'] = remitente
        msg['To'] = data['email']
        msg.set_content(f"Hola {data['nombre']},\n\nTu código de acceso seguro es: {codigo}")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(remitente, password)
                smtp.send_message(msg)
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()

with socketserver.TCPServer(("", 8080), MyHandler) as httpd:
    print("Servidor U-KEY activo en el puerto 8080")
    httpd.serve_forever()

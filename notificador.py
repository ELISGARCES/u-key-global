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
            
            # REVISA ESTO ELIS: ¿Tu correo es exactamente este?
            remitente = "elisgarces1966@gmail.com"
            # REVISA ESTO ELIS: ¿La contraseña de 16 letras es esta?
            password = "yyuy yugv tjbh fkms"
            
            msg = EmailMessage()
            msg['Subject'] = f'Codigo U-KEY: {codigo}'
            msg['From'] = remitente
            msg['To'] = data['email']
            msg.set_content(f"Hola {data['nombre']},\n\nTu codigo es: {codigo}")

            print(f"Intentando enviar correo a: {data['email']}") # Mensaje en LOGS
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(remitente, password)
                smtp.send_message(msg)
            
            print("¡CORREO ENVIADO CON EXITO!") # Mensaje en LOGS
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"codigo_servidor": codigo}).encode())
            
        except Exception as e:
            # ESTO ES LO QUE NECESITO QUE ME COPIES DESPUES
            print(f"DIAGNOSTICO_FALLO: {str(e)}") 
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

puerto = int(os.environ.get("PORT", 10000))
with socketserver.TCPServer(("", puerto), MyHandler) as httpd:
    print(f"Servidor arrancado en puerto {puerto}")
    httpd.serve_forever()

import http.server
import socketserver
import json
import os

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        # Aquí irá la lógica del correo, pero primero aseguremos que el servidor ARRANQUE
        response = {"status": "success", "message": "Servidor U-KEY en linea"}
        self.wfile.write(json.dumps(response).encode())

# ESTO ES LO QUE RENDER NECESITA PARA NO DAR ERROR
port = int(os.environ.get("PORT", 8080))
with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"U-KEY GLOBAL Activo en puerto {port}")
    httpd.serve_forever()

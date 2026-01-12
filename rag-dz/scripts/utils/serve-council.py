#!/usr/bin/env python3
"""
Serveur HTTP simple pour la landing page Council
Lance sur http://localhost:3000
"""
import http.server
import socketserver
import os

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════════════════╗
║         LLM COUNCIL - SERVEUR DÉMARRÉ                    ║
╠══════════════════════════════════════════════════════════╣
║  📍 URL:  http://localhost:{PORT}/council-standalone.html  ║
║  📂 Dir:  {DIRECTORY[:40]:<40} ║
║  🛑 Stop: Ctrl+C                                         ║
╚══════════════════════════════════════════════════════════╝
        """)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Serveur arrêté")

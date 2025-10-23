from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket
from datetime import datetime

CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = 3000
RESULT_FILE = "resultados.txt"

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())

        elif self.path == "/people":
            cmd = {"method": "GET"}
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((CLIENT_HOST, CLIENT_PORT))
                    s.sendall(json.dumps(cmd).encode())
                    response = s.recv(8192).decode()
                    result = json.loads(response) if response.strip().startswith("{") else response
            except Exception as e:
                result = {"error": str(e)}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif self.path == "/resultados":
            try:
                with open(RESULT_FILE, "r", encoding="utf-8") as f:
                    conteudo = f.read()
            except FileNotFoundError:
                conteudo = "Nenhum resultado encontrado ainda."
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/run":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())

            name = data.get("name", "Desconhecido")
            age = data.get("age", 0)

            cmd = {"method": "POST", "data": {"name": name, "age": age}}
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((CLIENT_HOST, CLIENT_PORT))
                    s.sendall(json.dumps(cmd).encode())
                    response = s.recv(4096).decode()
                    result = json.loads(response)
            except Exception as e:
                result = {"error": str(e)}

            with open(RESULT_FILE, "a", encoding="utf-8") as f:
                f.write(
                    f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - "
                    f"Nome: {name}, Idade: {age}, "
                    f"Sync: {result.get('sync_avg', 0):.2f} ms, "
                    f"Async: {result.get('async_avg', 0):.2f} ms, "
                    f"Média: {result.get('media', 0):.2f} ms\n"
                )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()


def run():
    server = HTTPServer(("0.0.0.0", 80), WebServer)
    server.serve_forever()

if __name__ == "__main__":
    run()

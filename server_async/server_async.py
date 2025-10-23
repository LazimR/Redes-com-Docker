import socket
import hashlib
import threading
import time
from datetime import datetime
import json as _json


HOST="0.0.0.0"
PORT=80
LOG_FILE = "server_async_log.txt"

class server_async():
    def __init__(self) -> None:
        self.x_code = self.generate_id()
        self.create_log_file()

    def generate_id(self):
        encode_id = "20219004610 Lazaro".encode()
        return hashlib.md5(encode_id).hexdigest()

    def create_log_file(self):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{'='*50}\n")
            f.write(f"LOG INICIADO EM {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"{'='*50}\n")

    def log_request(self, addr, method, path, status_code, duration_ms):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%H:%M:%S")
            f.write(
                f"[{timestamp}] {addr[0]}:{addr[1]} "
                f"{method} {path} => {status_code} "
                f"({duration_ms:.2f} ms)\n"
            )
    def process_requisition(self,req:str):
        data = req.split("\r\n")
        method, path, version = data[0].split(" ")
        if not data or len(data[0].split(" ")) < 3:
            return "HTTP/1.1 400 Bad Request\r\n\r\n", "400", "UNKNOWN", "UNKNOWN"

        if version != "HTTP/1.1": return "HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n"

        match method:
            case "GET":
                match path:
                    case "/":
                        status_code = "200"
                        message = "OK"
                        body = "Welcome to Lazarus Server!"
                        content_type = "text/plain"
                    case "/people":
                        body = _json.dumps([
                            {"name": "João", "age": 25},
                            {"name": "Maria", "age": 30}
                        ])
                        content_type = "application/json"
                        status_code = "200"
                        message = "OK"
                    case _:
                        status_code = "404"
                        message = "Not Found"
                        body = "Pathing not found"
                        content_type = "text/plain"
                response = (
                    f"HTTP/1.1 {status_code} {message}\r\n"
                    f"Content-Type: {content_type}"
                    f"Content-Length: {len(body)}\r\n"
                    f"X-Custom-ID: {self.x_code}\r\n"
                    f"Connection: close\r\n"
                    f"Server: Lazarusasync/1.0\r\n"
                    "\r\n"
                    f"{body}"
                )
            case "POST":
                if path == "/people":
                    body = _json.dumps({"message": "Pessoa criada com sucesso"})
                    status_code = "201"
                    message = "Created"
                    content_type = "application/json"
                else:
                    body = "Endpoint não implementado"
                    status_code = "404"
                    message = "Not Found"
                    content_type = "text/plain"
                response = (
                    f"HTTP/1.1 {status_code} {message}\r\n"
                    f"Content-Type: {content_type}"
                    f"Content-Length: {len(body)}\r\n"
                    f"X-Custom-ID: {self.x_code}\r\n"
                    f"Connection: close\r\n"
                    f"Server: Lazarusasync/1.0\r\n"
                    "\r\n"
                    f"{body}"
                )
            case "DELETE":
                response = "HTTP/1.1 501 Not Implemented\r\n\r\n"
                status_code = "501"
            case "PUT":
                response = "HTTP/1.1 501 Not Implemented\r\n\r\n"
                status_code = "501"        
            case _:
                response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            
        return response, status_code, method, path

    def handle_client(self, conn, addr):
        inicio = time.time()
        try:
            req = conn.recv(2048).decode()
            response, status_code, method, path = self.process_requisition(req)
            conn.sendall(response.encode())
        except Exception as e:
            print(f"Erro ao atender {addr}: {e}")
            status_code, method, path = "500", "UNKNOWN", "UNKNOWN"
        finally:
            conn.close()
            fim = time.time()
            duracao_ms = (fim - inicio) * 1000
            self.log_request(addr, method, path, status_code, duracao_ms)
            print(f"[THREAD] {method} {path} -> {status_code} ({duracao_ms:.2f} ms)")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((HOST, PORT))
            server.listen(5)
            print(f"Servidor concorrente ativo em {HOST}:{PORT}")

            while True:
                conn, addr = server.accept()
                print(f"Nova conexão de {addr}")
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()

if __name__ == "__main__":
    server = server_async()
    server.start()

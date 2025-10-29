import socket
import json
import time
from datetime import datetime

HOST = "localhost"
PORT = 3000
LOG_FILE = "client_log.txt"

class Client:
    def __init__(self, sync_ip: str, async_ip: str, port: int = 80, num_requests: int = 10):
        self.server_sync_ip = sync_ip
        self.server_async_ip = async_ip
        self.port = port
        self.num_requests = num_requests
        self.create_log_file()

    def create_log_file(self):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{'='*60}\n")
            f.write(f"CLIENTE INICIADO EM {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"{'='*60}\n")

    def log(self, message: str):
        print(message)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def build_request(self, method="GET", path="/", data=None):
        if method == "POST":
            body = json.dumps(data or {"msg": "teste"})
            return (
                f"POST {path} HTTP/1.1\r\n"
                f"Host: localhost\r\n"
                f"Content-Type: application/json\r\n"
                f"Content-Length: {len(body)}\r\n"
                f"Connection: close\r\n"
                "\r\n"
                f"{body}"
            )
        else:
            return (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: localhost\r\n"
                f"Connection: close\r\n"
                "\r\n"
            )

    def send_request(self, server_ip: str, request: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, self.port))
            s.sendall(request.encode())
            response = s.recv(4096).decode(errors="ignore")
        headers, _, body = response.partition("\r\n\r\n")
        status_line = headers.split("\r\n")[0] if "\r\n" in headers else headers.split("\n")[0]
        try:
            http_version, status_code, status_message = status_line.split(" ", 2)
        except ValueError:
            status_code = "???"
            status_message = status_line
        return status_code, status_message, body

    def run_test(self, server_ip: str, method="GET", data=None):
        tempos = []
        for _ in range(self.num_requests):
            
            try:
                inicio = time.time()
                req = self.build_request(method, "/", data)
                status_code, status_message, body = self.send_request(server_ip, req)
                fim = time.time()
                self.log(f"Servidor { "Sincrono" if (server_ip == "46.10.0.2") else "Assincrono" } | Resposta: Código {status_code} - {status_message} | Corpo: {body} | Tempo: {(fim - inicio) * 1000} ms")
                tempos.append((fim - inicio) * 1000)
            except Exception as e:
                self.log(f"Erro: {e}")
                continue     
        return sum(tempos) / len(tempos) if tempos else 0

    def execute(self, method="GET", data=None):
        self.log(f"\n== Teste solicitado: {method} ==")
        sync_avg = self.run_test(self.server_sync_ip, method, data)
        async_avg = self.run_test(self.server_async_ip, method, data)
        self.log(f"Sync: {sync_avg:.2f} ms | Async: {async_avg:.2f} ms")
        return {"sync_avg": sync_avg, "async_avg": async_avg}

def main():
    client = Client("46.10.0.2", "46.10.0.3", port=80)

    client.execute(method="GET")  # ou "POST" se desejar, pode customizar

if __name__ == "__main__":
    main()

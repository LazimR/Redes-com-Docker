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
        return response

    def run_test(self, server_ip: str, method="GET", data=None):
        tempos = []
        for _ in range(self.num_requests):
            inicio = time.time()
            try:
                req = self.build_request(method, "/", data)
                _ = self.send_request(server_ip, req)
            except Exception as e:
                self.log(f"Erro: {e}")
                continue
            fim = time.time()
            tempos.append((fim - inicio) * 1000)
        return sum(tempos) / len(tempos) if tempos else 0

    def execute(self, method="GET", data=None):
        self.log(f"\n== Teste solicitado: {method} ==")
        sync_avg = self.run_test(self.server_sync_ip, method, data)
        async_avg = self.run_test(self.server_async_ip, method, data)
        media = (sync_avg + async_avg) / 2
        self.log(f"Sync: {sync_avg:.2f} ms | Async: {async_avg:.2f} ms | Média: {media:.2f} ms")
        return {"sync_avg": sync_avg, "async_avg": async_avg, "media": media}

def start_server():
    client = Client("46.10.0.2", "46.10.0.3", port=80)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Cliente aguardando comandos em {HOST}:{PORT}")
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"Conexão recebida de {addr}")
                data = conn.recv(4096).decode()
                try:
                    cmd = json.loads(data)
                    method = cmd.get("method", "GET").upper()
                    payload = cmd.get("data", None)
                    result = client.execute(method, payload)
                    conn.sendall(json.dumps(result).encode())
                except Exception as e:
                    err = {"error": str(e)}
                    conn.sendall(json.dumps(err).encode())

if __name__ == "__main__":
    start_server()

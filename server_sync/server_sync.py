from email import message
from email.policy import default
import socket
import hashlib

HOST="0.0.0.0"
PORT=80



class server_sync():
    def __init__(self) -> None:
        self.x_code = self.gerar_id()

    def generate_id():
        encode_id = "20219004610 Lazaro".encode()
        return hashlib.md5(encode_id).hexdigest()

    def process_requisition(req:str):
        data = req.split("\r\n")
        method, path, version = data[0].split(" ")

        if version != "HTTP/1.1": return "HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n"

        match method:
            case "GET":
                match path:
                    case "/":
                        status_code = "200"
                        message = "OK"
                        body = "Welcome to Lazarus Server!"
                        content_type = "text/plain"
                    case _:
                        status_code = "404"
                        message = "Not Found"
                        body = "Pathing not found"
                        content_type = "text/plain"
                response = (
                    f"HTTP/1.1 {status_code} {body}\r\n"
                    f"Content-Type: {content_type}"
                    f"Conten-Length: {len(body)}\r\n"
                    "\r\n"
                    f"{body}"

                )
            case "POST":
                pass
            case "DELETE":
                pass
            case "PUT":
                pass        
            case _:
                response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            
        return response
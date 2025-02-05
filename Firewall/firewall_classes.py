import socket
import threading
import ssl
from ssl import SSLError, SSLContext
import requests

BUFFER_SIZE = 4096
ALLOWED_IPS = ("127.0.0.1", "192.168.1.56", "192.168.1.100")

FLASK_PORT = 5000
FTP_PORT = 2121

def check_ip_address(connection, client_ip) -> bool:
    '''True if the client_ip is in the ALLOWED_IPS list, False otherwise'''
    if isinstance(connection, FTP_handler):
        if client_ip not in ALLOWED_IPS:
            print(f"❌ BLOCKED: {client_ip}")
            return False
        print(f"✅ ALLOWED: Forwarding {client_ip} to FTP server on port 2121")
        return True
    if isinstance(connection, HTTPS_handler):
        if client_ip not in ALLOWED_IPS:
            print(f"❌ BLOCKED: {client_ip}")
            return False
        print(f"✅ ALLOWED: Forwarding {client_ip} to Flask server on port 5000")
        return True
    return False

class FTP_handler():
    def __init__(self, listen_port = 5200):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", listen_port))
        self.server_socket.listen(5)
        
    def ftp_start(self):
        while True:
            print("Waiting for a FTP connection...")
            client_socket, client_address = self.server_socket.accept()
            print(f"FTP Connection from {client_address} accepted")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
    
    def handle_client(self, client_socket: socket.socket, client_address):
        if not check_ip_address(self, client_address[0]):
            client_socket.close()
            return
        
        # establish connection with the FTP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ftp_socket:
            try:
                ftp_socket.connect(("127.0.0.1", FTP_PORT))
                print("FTP Connection to FTP server established") # <--- till here it works
                client_socket.sendall(b"220 Connection established\n")
                while True:
                    part = client_socket.recv(BUFFER_SIZE) # stack here
                    if not part:
                        break
                    ftp_socket.sendall(part)
                    part = ftp_socket.recv(BUFFER_SIZE)
                    if not part:
                        break
                    client_socket.sendall(part)
            except Exception as e:
                print(f"Error while connecting to FTP server: {e}")
                client_socket.close()
                return
        client_socket.close()
        

class HTTPS_handler():
    def __init__(self, listen_port = 5100):
        self.context = ssl.SSLContext()
        self.context.load_cert_chain("cert.pem", "key.pem")
        self.server_socket = self.generate_secure_socket(listen_port)
        
    def generate_secure_socket(self, listen_port):
        '''Generates a secure socket for https connections'''
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", listen_port))
        server_socket.listen(5)
        return self.context.wrap_socket(server_socket, server_side=True)
    
    def https_start(self):
        while True:
            print("Waiting for a https connection...")
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"HTTPS Connection from {client_address} accepted")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except SSLError:
                print("Non-HTTPS connection detected")
                continue
            
    def communicate_to_flask(self, client_socket: socket.socket, client_request: bytes) -> None:
        '''Send the client request to the Flask server'''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as flask_socket:
            try:
                flask_socket.connect(("127.0.0.1", FLASK_PORT))
                flask_socket.sendall(client_request)
                while part := flask_socket.recv(BUFFER_SIZE):
                    client_socket.sendall(part) ### OCCHIO CHE QUA È DIVERSO DAL CODICE ORIGINALE
            except Exception as e:
                print(f"Error while connecting to Flask server: {e}")
                client_socket.close()
                return
        return
    
    def receive_from_client(self, client_socket: socket.socket) -> bytes:
        '''Receive and return the client request'''
        start_line__header = b""
        try:
            while start_line__header[-4:] != b'\r\n\r\n':
                start_line__header += client_socket.recv(BUFFER_SIZE)
            if b'GET' in start_line__header:
                return start_line__header
            lines = start_line__header.split(b'\r\n')
            headers = {}
            for line in lines[1:]:
                if line == b'':
                    break
                key, value = line.split(b':', 1) # <--- Split solo alla prima occorrenza
                headers[key] = value
            if b'Content-Length' not in headers.keys():
                print("Content-Length non presente")
                return False # <--- Se non c'è Content-Length, non possiamo ricevere il body
            body = client_socket.recv(int(headers[b'Content-Length']))
            return start_line__header + body
        except Exception as e:
            print(f"Error while receiving from client: {e}")
            client_socket.close()
            return False

        
    def handle_client(self, client_socket, client_address):
        '''Handle the client connection'''
        if not check_ip_address(self, client_address[0]):
            client_socket.close()
            return
        
        try:
            client_request = self.receive_from_client(client_socket)
            if not client_request:
                return
            self.communicate_to_flask(client_socket, client_request)
            
        except Exception as e:
            print(f"Error while receiving from client: {e}")
            client_socket.close()
            return
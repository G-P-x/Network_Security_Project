import socket
import threading
from ssl import SSLError, SSLContext

BUFFER_SIZE = 4096
ALLOWED_IPS = ("127.0.0.1")

FLASK_PORT = 5000
FTP_PORT = 2121

def check_ip_address(connection, client_ip, allowed_ips = ALLOWED_IPS) -> bool:
    '''True if the client_ip is in the ALLOWED_IPS list, False otherwise'''
    if isinstance(connection, FTP_handler):
        if client_ip not in allowed_ips:
            print(f"❌ BLOCKED --- Anauthorised IP Address detected: {client_ip}")
            return False
        print(f"✅ ALLOWED: Forwarding {client_ip} to FTP server on port 2121")
        return True
    if isinstance(connection, HTTPS_handler):
        if client_ip not in allowed_ips:
            print(f"❌ BLOCKED --- Anauthorised IP Address detected: {client_ip}")
            return False
        print(f"✅ ALLOWED: Forwarding {client_ip} to Flask server on port 5000")
        return True
    return False

class FTP_handler():
    def __init__(self, listen_port = 5200, allowed_ips = ALLOWED_IPS):
        self.allowed_ips = allowed_ips
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", listen_port))
        self.server_socket.listen(5)
        
    def ftp_start(self):
        while True:
            print("Waiting for a FTP connection...")
            client_socket, client_address = self.server_socket.accept()
            print(f"TCP handshake from {client_address} accepted")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def close_connection(self, client_socket: socket.socket, ftp_socket = None) -> None:
        '''Close the client and FTP server connections'''
        
        client_socket.close()
        if isinstance(ftp_socket, socket.socket):
            ftp_socket.close()
        return
    
    def handle_client(self, client_socket: socket.socket, client_address):
        if not check_ip_address(self, client_address[0], self.allowed_ips):
            client_socket.close()
            return
        
        # establish connection with the FTP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ftp_socket:
            try:               
                # DO: receive the first command from the client and analyze it
                client_socket.sendall(b"220 Connection established\n") # <--- Send the response to the client saying that the connection is established
                part = client_socket.recv(BUFFER_SIZE) # now I expect the client to send the first command
                # analyze the command
                if not b'USER' in part[:4]:
                    print("❌ BLOCKED: Non-FTP connection detected")
                    client_socket.sendall(b"You're not allowed to connect to the server\n")
                    self.close_connection(client_socket)
                    return
                # if b'SSH' in part[:3]:
                #     print("❌ BLOCKED: SSH connection detected")
                #     return

                # Me firewall connects to the local ftp server to send the command
                ftp_socket.connect(("127.0.0.1", FTP_PORT))
                confirm_ftp = ftp_socket.recv(BUFFER_SIZE) # expected 220
                if b'220' not in confirm_ftp:
                    print("Error while connecting to FTP server")
                    client_socket.sendall(b'505 Error with the FTP server, closing connection...\r\n')
                    client_socket.close()
                    return
                print("firewall connection to FTP server established")           
                ftp_socket.sendall(part) 
                # DO: receive the response from the FTP server and send it to the client
                part = ftp_socket.recv(BUFFER_SIZE)
                client_socket.sendall(part)
                # DO: keep the connection open and forward the commands and responses between the client and the FTP server             
                while True:
                    part = client_socket.recv(BUFFER_SIZE) 
                    if not part:
                        client_socket.close()
                        ftp_socket.close()
                        break
                    if b'STOR' in part[:4]: # <--- If the command is STOR, the firewall blocks the connection
                        print("❌ BLOCKED: STOR command detected")
                        client_socket.sendall(b"STOR command is not allowed, closing connection\n")
                        client_socket.close()
                        ftp_socket.close()
                        break
                    ftp_socket.sendall(part)
                    part = ftp_socket.recv(BUFFER_SIZE)
                    if not part:
                        client_socket.close()
                        ftp_socket.close()
                        break
                    client_socket.sendall(part)
            except Exception as e:
                print(f"Error while connecting to FTP server: {e}")
                client_socket.close()
                return
        client_socket.close()
        

class HTTPS_handler():
    def __init__(self, listen_port = 5100, allowed_ips = ALLOWED_IPS):
        self.allowed_ips = allowed_ips
        self.context = SSLContext()
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
                print(f"TCP Handshake from {client_address} accepted")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except SSLError:
                print("❌ BLOCKED: Non-HTTPS connection detected")
                # client_socket.close()
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
        '''Receive and return the client request and inspect it'''
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
            if b'Content-Length' not in headers.keys() or int(headers[b'Content-Length']) == 0:
                print("❌ BLOCKED: Content-Length header not present or empty")
                client_socket.sendall(b"Data error, closing connection...\n")
                client_socket.close()
                return False # <--- Se non c'è Content-Length, non possiamo ricevere il body
            body = client_socket.recv(int(headers[b'Content-Length']))
            print(f"✅ ALLOWED payload: {body}")
            return start_line__header + body
        except Exception as e:
            print(f"❌ BLOCKED: 400 Bad Request, error while receiving from client: {e}")
            client_socket.close()
            return False

        
    def handle_client(self, client_socket: socket.socket, client_address):
        '''Handle the client connection'''
        if not check_ip_address(self, client_address[0], self.allowed_ips):
            client_socket.sendall(b"You're not allowed to connect to the server, closing connection...\n")
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

if __name__ == "__main__":
    HTTPS_LISTEN_PORT = 5100
    FTP_LISTEN_PORT = 5200
    ALLOWED_IPS = ("127.0.0.1", "192.168.1.56", "192.168.1.100")
    ftp_handler = FTP_handler(FTP_LISTEN_PORT, ALLOWED_IPS)
    ftp_thread = threading.Thread(target=ftp_handler.ftp_start)
    https_handler = HTTPS_handler(HTTPS_LISTEN_PORT, ALLOWED_IPS)
    ftp_thread.start()
    https_handler.https_start()
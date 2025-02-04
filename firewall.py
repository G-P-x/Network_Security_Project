import socket
import threading
import ssl
from ssl import SSLError, SSLContext
import requests

LISTEN_PORT = 5100
FLASK_PORT = 5000
ALLOWED_IPS = ("127.0.0.1", "192.168.1.56", "192.168.1.100", "10.50.169.158", "192.168.1.174")

def receive_data_from_client(client_socket: socket.socket) -> bytes: 
    '''Returns the data received from the client as a buffer'''   
    try:
        print("Ricezione dati dal client")
        # ricezione header
        start_line__header = b''
        while start_line__header[-4:] != b'\r\n\r\n':
            start_line__header += client_socket.recv(4096)
        print(f"Header ricevuto dal client: {start_line__header.decode()}")
        lines = start_line__header.split(b'\r\n')
        start_line = lines[0]
        if b'GET' in start_line:
            print("GET request")
            return start_line__header
        headers = {}
        for line in lines[1:]:
            if line == b'':
                break
            key, value = line.split(b':', 1) # <--- Split solo alla prima occorrenza
            headers[key] = value
            
        if b'Content-Length' not in headers.keys():
            print("Content-Length non presente")
            return start_line__header # qua potrei mettere un return None o un raise Exception perché una post request senza body non ha senso
        # ricezione body
        body = client_socket.recv(int(headers[b'Content-Length']))
        client_request = start_line__header + body
        return client_request
        # while True:
        #     client_request += client_socket.recv(4096) # il problema è qui, quando non riceve più dati si blocca perché sto figlio di troia è bloccante
        #     # CI PIAZZO IO UNA CONDIZIONE DI USCITA
        #     if client_request[-1:] == b'}': # <--- Condizione di uscita CHE FUNZIONA SOLO SE IL CLIENT MANDA UN JSON
        #         break
        # # client_request = b'POST /debug_path_post HTTP/1.1\r\nHost: 127.0.0.1:5100\r\nUser-Agent: python-requests/2.32.3\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\nContent-Length: 83\r\nContent-Type: application/json\r\n\r\n{"username": "username", "password": "password", "altri dati": "altri dati a caso"}'
        
    except Exception as e:
        print(f"Errore durante la ricezione dal client: {e}")
        client_socket.close()
        return None
    except socket.timeout as e:
        print(f"Timeout durante la ricezione dal client: {e}")
        client_socket.close()
        return None
    except SSLError as e:
        print(f"Errore SSL durante la ricezione dal client: {e}")
        client_socket.close()
        return None

def check_ip_address(client_ip) -> bool:
    '''True if the client_ip is in the ALLOWED_IPS list, False otherwise'''
    if client_ip not in ALLOWED_IPS:
        print(f"❌ BLOCKED: {client_ip} tried to access port {LISTEN_PORT}")
        return False
    print(f"✅ ALLOWED: Forwarding {client_ip} to Flask server on port {FLASK_PORT}")
    return True
    
    
def send_data_to_client(client_socket: socket.socket, data):
    try:
        client_socket.sendall(data) # <--- Invia la risposta al client in HTTP
    except Exception as e:
        print(f"Errore durante l'invio al client: {e}")
        client_socket.close()

def handle_client(client_socket: socket.socket, client_address):
    """Gestisce un singolo client per thread."""
    if not check_ip_address(client_address[0]):
        client_socket.close()
        return

    client_request = receive_data_from_client(client_socket)   
    

    # Connettiti al server Flask (HTTP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as flask_socket:
        try:
            flask_socket.connect(("127.0.0.1", FLASK_PORT))
            # Inoltra la richiesta DECRITTOGRAFATA al server Flask
            
            flask_socket.sendall(client_request)  # <--- Inoltra la richiesta al server Flask (HTTP)
            flask_response = b""  # Ricevi la risposta dal server Flask (HTTP)
            while part := flask_socket.recv(4096):
                flask_response += part
            print("flask response:\n{}".format(flask_response.decode()))
        except Exception as e:
            print(f"Errore durante la comunicazione col il server Flask: {e}")
            client_socket.close()
            return

    try:
        client_socket.sendall(flask_response)  # <--- Invia la risposta al client (che è ancora connesso tramite HTTPS)
        print("Risposta inviata al client")
    except Exception as e:
        print(f"Errore durante l'invio al client: {e}")
        client_socket.close()
        return
    # chiudo i socket qualora non siano già stati chiusi
    try:
        client_socket.close()
    except:
        pass
    try:
        flask_socket.close()
    except:
        pass
    print(f"Connessione da {client_address} chiusa")


def start_firewall():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # nodo dove agisce il firewall
        server_socket.bind(("0.0.0.0", LISTEN_PORT))
        server_socket.listen(5)
        print(f"Firewall proxy listening on port {LISTEN_PORT}")
        
        context = SSLContext()
        context.load_cert_chain("cert.pem", "key.pem")  # <--- Carica i file cert.pem e key.pem
        secure_server_socket = context.wrap_socket(server_socket, server_side=True)  # <--- Usa il contesto
    
    except Exception as e:
        print(f"Errore durante l'avvio del firewall: {e}")

    while True:
        print("Waiting for a connection...")
        try:
            client_socket, client_address = secure_server_socket.accept()  # <--- Accetta la connessione
            print(f"HTTPS Connection from {client_address} accepted")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except SSLError:
            print("Non-HTTPS connection detected")
            # client_socket is not created
            continue


if __name__ == "__main__":
    start_firewall()
    # try connection with the server
    # send_post_request_to_server({"username": "username", "password": "password"})
    
    
    # POST /debug_path_post HTTP/1.1
    # Host: 127.0.0.1:5100
    # User-Agent: python-requests/2.32.3
    # Accept-Encoding: gzip, deflate
    # Accept: */*
    # Connection: keep-alive
    # Content-Length: 58
    # Content-Type: application/json

    # "{\"username\": \"username\", \"password\": \"password\"}"
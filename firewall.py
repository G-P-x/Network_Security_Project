import socket
import threading

LISTEN_PORT = 5100
FLASK_PORT = 5000
ALLOWED_IPS = ("127.0.0.1", "192.168.1.56", "192.168.1.100", "10.131.0.64")

def handle_client(client_socket: socket.socket, client_address):
    try:
        client_ip = client_address[0]
        if client_ip not in ALLOWED_IPS:
            print(f"❌ BLOCKED: {client_ip} tried to access port {LISTEN_PORT}")
            client_socket.close()
            return
        
        print(f"✅ ALLOWED: Forwarding {client_ip} to Flask server on port {FLASK_PORT}")

        # Connect to the Flask server
        flask_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flask_socket.connect(("127.0.0.1", FLASK_PORT))

        # Forward the client's request to the Flask server
        client_request = client_socket.recv(4096)
        flask_socket.sendall(client_request)

        # Get response from Flask and send it back to the client
        while True:
            flask_response = flask_socket.recv(4096)
            if not flask_response:
                break
            client_socket.sendall(flask_response)

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")

    finally:
        # Close the sockets
        client_socket.close()
        flask_socket.close()
        print(f"Connection from {client_address} closed")

def start_firewall():
    # create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create the network node
    server_socket.bind(("0.0.0.0", LISTEN_PORT)) # bind the network node to the port, it listens to all the interfaces
    server_socket.listen(5) # listen to a maximum of 5 connections

    print(f"Firewall proxy listening on port {LISTEN_PORT}")

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_firewall()

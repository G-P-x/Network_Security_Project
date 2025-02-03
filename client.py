import socket
import requests

SERVER_IP = "127.0.0.1"  # Replace with the actual server IP
SERVER_PORT = 5100            # Port of the firewall proxy

def send_request():
    request = "GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(SERVER_IP)

    # Create a socket connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the firewall proxy
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to {SERVER_IP}:{SERVER_PORT}")

        # Send the HTTP request
        client_socket.sendall(request.encode())

        # Receive the response
        response = b""
        while True:
            part = client_socket.recv(4096)
            if not part:
                break
            response += part

        # Print the full response
        print("Response from server:")
        print(response.decode())

    except ConnectionRefusedError:
        print("Connection refused. The server may be blocking this request.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # send_request()
    response = requests.get('http://127.0.0.1:5100/')
    print(response.text)


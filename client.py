import socket
import requests

SERVER_IP = "10.131.0.64"  # Replace with the actual server IP <---- your IP ADDRESS in the network
SERVER_PORT = 5100            # Port of the firewall proxy

if __name__ == "__main__":
    response = requests.get('http://127.0.0.1:5100/')
    print(response.text)

    response_2 = requests.post(f"http://{SERVER_IP}:{SERVER_PORT}/test_post", json={'username':'giovanni'})
    print(response_2.text)


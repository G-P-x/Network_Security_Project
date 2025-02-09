from ftplib import FTP
from sqlite3 import connect
import requests
        
def connect_to_server(server):
    try:
        response_2 = requests.get(server)
        print(response_2.text)
        print(response_2.status_code)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    HTTPS_port = "5100"
    FTP_port = "5200"
    server_1 = "http://127.0.0.1:" + HTTPS_port
    server_2 = "http://127.0.0.1:" + FTP_port
    connect_to_server(server_1)
    connect_to_server(server_2)
    

# connect directly to the flask server
# response = requests.post("http://127.0.0.1:5000/debug_path_post", json=good_data)
# print(response.text)
# print(response.status_code)
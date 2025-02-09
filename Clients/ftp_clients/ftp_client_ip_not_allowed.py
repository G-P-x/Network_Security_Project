import socket
import os
import sys
# Add the Clients directory to the path so I can import get_local_ip
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from get_local_ip import get_local_ip

def send_command(sock, command):
    """Invia un comando al server FTP e ritorna la risposta."""
    sock.sendall(command.encode('utf-8') + b'\r\n')
    response = sock.recv(4096).decode('utf-8')
    return response

def connect_ftp(server, port):
    """Connette al server FTP e ritorna il socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    return sock

def login_ftp(sock, username, password):
    """Effettua il login al server FTP."""
    response = send_command(sock, f'USER {username}')
    print(response)
    response = send_command(sock, f'PASS {password}')
    print(response)

def list_files(sock):
    """Elenca i file nella directory corrente."""
    response = send_command(sock, 'PASV')
    print(response)
    start = response.find('(') + 1
    end = response.find(')', start)
    pasv_info = response[start:end].split(',')
    pasv_ip = '.'.join(pasv_info[:4])
    pasv_port = (int(pasv_info[4]) << 8) + int(pasv_info[5])

    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((pasv_ip, pasv_port))

    response = send_command(sock, 'LIST')
    print(response)

    data_response = data_sock.recv(4096).decode('utf-8')
    print(data_response)

    data_sock.close()

def download_file(sock, filename):
    """Scarica un file dal server FTP."""
    response = send_command(sock, 'PASV')
    print(response)
    start = response.find('(') + 1
    end = response.find(')', start)
    pasv_info = response[start:end].split(',')
    pasv_ip = '.'.join(pasv_info[:4])
    pasv_port = (int(pasv_info[4]) << 8) + int(pasv_info[5])

    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((pasv_ip, pasv_port))

    response = send_command(sock, f'RETR {filename}')
    print(response)

    with open("Clients/temp/" + filename, 'wb') as f:
        while True:
            data = data_sock.recv(4096)
            if not data:
                break
            f.write(data)

    data_sock.close()

def upload_file(sock, filename):
    """Carica un file sul server FTP."""
    response = send_command(sock, 'PASV')
    print(response)
    start = response.find('(') + 1
    end = response.find(')', start)
    pasv_info = response[start:end].split(',')
    pasv_ip = '.'.join(pasv_info[:4])
    pasv_port = (int(pasv_info[4]) << 8) + int(pasv_info[5])

    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((pasv_ip, pasv_port))

    response = send_command(sock, f'STOR {filename}')
    print(response)

    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            data_sock.sendall(data)

    data_sock.close()

def main():
    server = get_local_ip()
    if server == '127.0.0.1':
        print("Connect to the network to use this client")
        return
    port = 5200
    username = 'anonymous'
    password = 'user@example.com'
    filename = 'file.txt'

    try:
        sock = connect_ftp(server, port)
        response = sock.recv(4096).decode('utf-8')
        print(response)

        login_ftp(sock, username, password)
        download_file(sock, filename)

        send_command(sock, 'QUIT')
        sock.close()
    except Exception as e:
        print(f"Errore durante la connessione al server FTP: {e}")

if __name__ == '__main__':
    main()
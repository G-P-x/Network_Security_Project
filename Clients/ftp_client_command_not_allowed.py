import socket

def send_command(sock, command):
    """Invia un comando al server FTP e ritorna la risposta."""
    print("CLIENT: sending {command}".format(command=command))
    sock.sendall(command.encode('utf-8') + b'\r\n')
    response = sock.recv(4096).decode('utf-8')
    print("SERVER: {response}".format(response=response))
    return response

def connect_ftp(server, port):
    """Connette al server FTP e ritorna il socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    return sock

def login_ftp(sock, username, password):
    """Effettua il login al server FTP."""
    response = send_command(sock, f'USER {username}')
    response = send_command(sock, f'PASS {password}')
    

def list_files(sock):
    """Elenca i file nella directory corrente."""
    response = send_command(sock, 'PASV')
    
    start = response.find('(') + 1
    end = response.find(')', start)
    pasv_info = response[start:end].split(',')
    pasv_ip = '.'.join(pasv_info[:4])
    pasv_port = (int(pasv_info[4]) << 8) + int(pasv_info[5])

    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((pasv_ip, pasv_port))

    response = send_command(sock, 'LIST')
    

    data_response = data_sock.recv(4096).decode('utf-8')
    print(data_response)

    data_sock.close()

def download_file(sock, filename):
    """Scarica un file dal server FTP."""
    response = send_command(sock, 'PASV')
    
    start = response.find('(') + 1
    end = response.find(')', start)
    pasv_info = response[start:end].split(',')
    pasv_ip = '.'.join(pasv_info[:4])
    pasv_port = (int(pasv_info[4]) << 8) + int(pasv_info[5])

    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((pasv_ip, pasv_port))

    response = send_command(sock, f'RETR {filename}')
    

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
    
    start = response.find('(') + 1
    end = response.find(')', start)
    pasv_info = response[start:end].split(',')
    pasv_ip = '.'.join(pasv_info[:4])
    pasv_port = (int(pasv_info[4]) << 8) + int(pasv_info[5])

    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((pasv_ip, pasv_port))

    response = send_command(sock, f'STOR {filename}')
    

    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            data_sock.sendall(data)

    data_sock.close()

def main():
    server = '127.0.0.1'
    port = 5200
    username = 'anonymous'
    password = 'user@example.com'
    filename = 'file.txt'

    try:
        sock = connect_ftp(server, port)
        response = sock.recv(4096).decode('utf-8')
        print("SERVER: " + response)
        

        login_ftp(sock, username, password)
        upload_file(sock, filename)
        download_file(sock, filename)

        send_command(sock, 'QUIT')
        sock.close()
    except Exception as e:
        print(f"Errore durante la connessione al server FTP: {e}")

if __name__ == '__main__':
    main()
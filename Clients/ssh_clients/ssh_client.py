import paramiko

def connect_ssh(server, port, username, password):
    """Connette al server SSH e ritorna il client SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, username, password)
    return client

def send_command(client, command):
    """Invia un comando al server SSH e ritorna la risposta."""
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode('utf-8')

def main(port=5200):
    server = '127.0.0.1'
    username = 'your_username'
    password = 'your_password'
    command = 'ls -l'

    try:
        client = connect_ssh(server, port, username, password)
        response = send_command(client, command)
        print(response)
        client.close()
    except Exception as e:
        print(f"Errore durante la connessione al server SSH: {e}")

if __name__ == '__main__':
    main(5200) # <--- Tried to connect to the FTP server.
    print()
    main(5100) # <--- Tried to connect to the HTTPS server.
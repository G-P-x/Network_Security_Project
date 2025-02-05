import socket

FTP_HOST = "127.0.0.1"
FTP_PORT = 2121  # FTP server port
BUFFER_SIZE = 4096

def ftp_send_command(sock, command):
    """Invia un comando FTP e restituisce la risposta del server."""
    sock.sendall((command + "\r\n").encode())  # I comandi FTP terminano con \r\n
    response = sock.recv(BUFFER_SIZE).decode()
    print(f"➡ Sent: {command}")
    print(f"⬅ Received: {response}")
    return response

def ftp_client():
    """Connette un client al server FTP e autentica l'utente."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Evita blocchi
        sock.connect((FTP_HOST, FTP_PORT))  # Connessione al server FTP
        print("✅ Connected to FTP server")

        # Riceve il messaggio iniziale del server (es. "220 Twisted FTP Server")
        server_response = sock.recv(BUFFER_SIZE).decode()
        print(f"⬅ Server: {server_response}")

        # Invio del comando USER
        response = ftp_send_command(sock, "USER anonymous")
        if "331" in response:  # 331 significa "Guest login ok, type your email as password"
            ftp_send_command(sock, "PASS user@example.com")  # Invio password

        # Lista dei file nella directory corrente
        ftp_send_command(sock, "PASV")  # Passa alla modalità passiva (necessaria per LIST)
        ftp_send_command(sock, "LIST")  # Lista file

        # Chiudere la connessione
        ftp_send_command(sock, "QUIT")
        sock.close()
        print("🔌 Disconnected from FTP server")

    except socket.timeout:
        print("⏳ Timeout: Il server non ha risposto in tempo.")
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    ftp_client()

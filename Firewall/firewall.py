import threading

HTTPS_LISTEN_PORT = 5100
FTP_LISTEN_PORT = 5200
ALLOWED_IPS = ("127.0.0.1", "192.168.1.56", "192.168.1.100")

from firewall_classes import HTTPS_handler, FTP_handler

def start_firewall():
    ftp_handler = FTP_handler(FTP_LISTEN_PORT, ALLOWED_IPS)
    ftp_thread = threading.Thread(target=ftp_handler.ftp_start)
    https_handler = HTTPS_handler(HTTPS_LISTEN_PORT, ALLOWED_IPS)
    ftp_thread.start()
    https_handler.https_start()

if __name__ == "__main__":
    start_firewall()
    # https_handler = HTTPS_handler(HTTPS_LISTEN_PORT)
    # https_handler.https_start()
    
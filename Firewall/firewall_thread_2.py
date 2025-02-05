import threading
HTTPS_LISTEN_PORT = 5100
FTP_LISTEN_PORT = 5200

from firewall_classes import HTTPS_handler, FTP_handler

if __name__ == "__main__":
    ftp_handler = FTP_handler(FTP_LISTEN_PORT)
    ftp_handler.ftp_start()
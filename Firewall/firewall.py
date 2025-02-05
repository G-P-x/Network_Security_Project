HTTPS_LISTEN_PORT = 5100
FTP_LISTEN_PORT = 5200

from firewall_classes import HTTPS_handler

if __name__ == "__main__":
    https_handler = HTTPS_handler(HTTPS_LISTEN_PORT)
    https_handler.https_start()
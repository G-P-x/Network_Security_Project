import socket
import sys

def connect_to_google():
    # Create a socket object
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err: 
        print("socket creation failed with error %s" %(err))

    # Define the port on which you want to connect
    port = 80

    try:
        host_ip = socket.gethostbyname('www.google.com')
    except socket.gaierror:
        # this means could not resolve the host
        print("there was an error resolving the host")
        sys.exit()

    # connect to the server
    s.connect((host_ip, port))
    print("the socket has successfully connected to google on port == %s" %(host_ip))

def connect_locally():
    # Create a socket object
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" %(err))

    # Define the port on which you want to connect
    port = 5000
    host_ip = '127.0.0.1'
    s.connect((host_ip, port))
    print(s.recv(1024).decode())
    print("the socket has successfully connected localHost on port == %s" %(port))
    s.close()

if __name__ == '__main__':
    connect_locally()
    # connect_to_google()
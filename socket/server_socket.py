import socket
import sys

s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

port = 5000
s_server.bind(('', port))
print("socket binded to %s" %(port))
s_server.listen(5)
print("socket is listening")

while True:
    c, addr = s_server.accept()
    print('Got connection from', addr)
    c.send('Thank you for connecting'.encode())
    c.close()
    break
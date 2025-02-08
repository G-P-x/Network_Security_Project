import socket

def get_local_ip():
    '''Returns the local IP address of the machine, 
    the localhost address if it fails.'''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external host
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error as e:
        print(f"Error getting local IP: {e}")
        return '127.0.0.1'

if __name__ == '__main__':
    local_ip = get_local_ip()
    if local_ip:
        print(f"Local IP address: {local_ip}")
    else:
        print("Could not determine local IP address.")

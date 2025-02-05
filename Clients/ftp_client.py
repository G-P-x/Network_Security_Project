from ftplib import FTP

try:
    ftp = FTP()
    ftp.connect("127.0.0.1", 5100)  # Connect to your FTP server on port 2121
    response = ftp.login("anonymous", "user@example.com")  # Login with credentials
    print(response)  # Should print "230 Login successful."
except Exception as e:
    print(f"Errore durante la connessione al server FTP: {e}")



# get the file
filename = "file.txt"

print(ftp.retrlines("LIST"))

with open("./Clients/" + filename, 'wb') as f:
    ftp.retrbinary(f"RETR {filename}", f.write)



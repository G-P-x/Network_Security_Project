from twisted.cred.checkers import AllowAnonymousAccess, InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.protocols.ftp import FTPFactory, FTPRealm

import os
current_directory = os.getcwd()
relative_path = "Public"
print(current_directory)

portal = Portal(FTPRealm(os.path.join(current_directory,relative_path)), [AllowAnonymousAccess()])

factory = FTPFactory(portal)

reactor.listenTCP(2121, factory)

if __name__ == "__main__":
    try:
        print("FTP server started on port 2121")
        reactor.run()
    except Exception as e:
        print(f"Error while starting FTP server: {e}")
        reactor.stop()

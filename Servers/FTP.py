from twisted.cred.checkers import AllowAnonymousAccess, InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.protocols.ftp import FTPFactory, FTPRealm

portal = Portal(FTPRealm("/home/giovanni/Desktop/MASTER_DEGREE_PROJECTS/Network_Security_Project/Public"), [AllowAnonymousAccess()])

factory = FTPFactory(portal)

reactor.listenTCP(2121, factory)

reactor.run()
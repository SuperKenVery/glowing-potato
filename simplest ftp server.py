from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
authorizer=DummyAuthorizer()
authorizer.add_anonymous("C:/users/sagat/desktop")
handler=FTPHandler
handler.authorizer=authorizer
server=FTPServer(('192.168.3.201',21),handler)
server.serve_forever()

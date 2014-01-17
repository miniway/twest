from twisted.web.server import Site
from twisted.internet import reactor
from twisted.application import service, internet
from routes import ROOT, RESOURCES
from twest.resource_builder import build

def getService(port):
    # create a RESOURCES to serve static files
    return internet.TCPServer(port, build(ROOT, RESOURCES))

if __name__ == '__main__':
    port = 8080
    reactor.listenTCP(port, build(ROOT, RESOURCES))
    reactor.run();

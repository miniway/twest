from twisted.web.server import Site
from twisted.internet import reactor
from twisted.application import service, internet
from routes import ROOT, RESOURCES
import resource_builder

def getService(port):
    # create a RESOURCES to serve static files
    return internet.TCPServer(port, resource_builder.build(ROOT, RESOURCES))

if __name__ == '__main__':
    port = 8080
    reactor.listenTCP(port, resource_builder.build(ROOT, RESOURCES))
    reactor.run();

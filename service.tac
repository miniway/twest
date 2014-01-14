# You can run this .tac file directly with:
#    twistd -ny service.tac

import os
import api_service
from twisted.application import service, internet
from twisted.web import static, server

port = 8080
# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("API")

# attach the service to its parent application
service = api_service.getService(port)
service.setServiceParent(application)

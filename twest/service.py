import os
from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker, MultiService
from twisted.application import internet

from twest.resource_builder import build, build_timers
from twest import config


class Options(usage.Options):
    optParameters = [
        ["port", "p", 8088, "The port number to listen on."],
        ["conf", "c", "config.ini", "Configuration file path"],
        ["timers", "t", "timers", "Timers module path"],
        ["routes", "r", "routes", "Routes module path"],
    ]


class Service(object):
    implements(IServiceMaker, IPlugin)
    #tapname = "collector"
    #description = "Collector Service"
    #options = Options

    def __init__(self, name, description, options):
        Service.tapname = name
        Service.description = description
        Service.options = options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """
        if not os.path.exists(options['conf']):
            raise OSError("Config File %s not found" % options['conf'])
        config.new_config(Service.tapname, options['conf'], _service = options)
        ms = MultiService()
        svr = internet.TCPServer(int(options["port"]), build(options['routes']))
        svr.setServiceParent(ms)
        for timer in build_timers(options['timers']):
            svr = internet.TimerService(*timer)
            svr.setServiceParent(ms)

        return ms

def make_service(name, description, options = Options):
    return Service(name, description, options)

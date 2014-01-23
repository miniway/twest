import logging
from twisted.python import log
from twisted.python.logfile import DailyLogFile

class LevelFileLogObserver(log.FileLogObserver):

    def __init__(self, f, level=logging.INFO):
        log.FileLogObserver.__init__(self, f)
        self.logLevel = level

    def emit(self, eventDict):
        if eventDict['isError']:
            level = logging.ERROR
        elif 'level' in eventDict:
            level = eventDict['level']
        else:
            level = logging.INFO
        if level >= self.logLevel:
            log.FileLogObserver.emit(self, eventDict)

def logger():
    f = logfile.DailyLogFile("twest.log", '/tmp', maxRotatedFiles=100)
    flobserver = LevelFileLogObserver(f)
    return flobserver.emit

# twistd invocation
# twistd --logger=twest.logger.logger

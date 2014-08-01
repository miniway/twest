import logging
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from twest.config import get_conf

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
    log_dir = get_conf('log', 'dir', '/tmp')
    log_file = get_conf('log', 'file', 'twest.log')
    max_rotate = int(get_conf('log', 'max_rotate', 100))

    f = logfile.DailyLogFile(log_file, log_dir, maxRotatedFiles=max_rotate)
    flobserver = LevelFileLogObserver(f)
    return flobserver.emit

# twistd invocation
# twistd --logger=twest.logger.logger

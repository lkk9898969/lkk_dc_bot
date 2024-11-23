from pathlib import Path
import logging


def loggerhandler(loggerName: str,
                  logfileName: str = ...,
                  cwd: str | Path = '.',
                  level='INFO',
                  logfile_level: str = ...,
                  attachConsole: bool = True,
                  attachLogfile: bool = True):
    level = matchlevel(level)
    if logfile_level == ...:
        logfile_level = level
    else:
        logfile_level = matchlevel(logfile_level)
    if logfileName == ...:
        logfile = (Path(cwd) / loggerName)
    else:
        logfile = (Path(cwd) / logfileName)

    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s : %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S')
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    if attachConsole:
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(level)
        consolehandler.setFormatter(formatter)
        logger.addHandler(consolehandler)
    if attachLogfile:
        filehandler = logging.FileHandler(logfile.as_posix() + '.log',
                                          encoding='utf-8')
        filehandler.setLevel(logfile_level)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger


def matchlevel(_level: str):
    match _level.upper():
        case 'DEBUG':
            level = logging.DEBUG
        case 'INFO':
            level = logging.INFO
        case 'WARNING':
            level = logging.WARNING
        case 'ERROR':
            level = logging.ERROR
        case 'CRITICAL':
            level = logging.CRITICAL
        case _:
            level = logging.INFO
    return level

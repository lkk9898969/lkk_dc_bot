import logging

def loggerhandler(loggername:str,logfilename:str=...,level = 'INFO', logfile_level:str = ... , consoleattach:bool = True , logfileattach=True):
    level=matchlevel(level)
    if logfile_level == ...:
        logfile_level = level
    else:
        logfile_level = matchlevel(logfile_level)
    if logfilename == ...:
        logfilename = loggername

    formatter=logging.Formatter(fmt='%(asctime)s %(levelname)s : %(message)s',datefmt='%Y/%m/%d %H:%M:%S')
    logger=logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)
    if consoleattach:
        consolehandler=logging.StreamHandler()
        consolehandler.setLevel(level)
        consolehandler.setFormatter(formatter)
        logger.addHandler(consolehandler)
    if logfileattach:
        filehandler=logging.FileHandler(logfilename+'.log',encoding='utf-8')
        filehandler.setLevel(logfile_level)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger

def matchlevel(_level:str):
    match _level.upper():
        case 'DEBUG':
            level=logging.DEBUG
        case 'INFO':
            level=logging.INFO
        case 'WARNING':
            level=logging.WARNING
        case 'ERROR':
            level=logging.ERROR
        case 'CRITICAL':
            level=logging.CRITICAL
        case _:
            level=logging.INFO
    return level
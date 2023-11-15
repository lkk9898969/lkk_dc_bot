import logging

def loggerhandler(loggername:str,logname:str,level = 'INFO'):
    match level.upper():
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
    logging.basicConfig(level=level,format='%(asctime)s %(levelname)s : %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')
    logger=logging.getLogger(loggername)
    filehandler=logging.FileHandler(logname+'.log',encoding='utf-8')
    formatter=logging.Formatter(fmt='%(asctime)s %(levelname)s : %(message)s',datefmt='%Y/%m/%d %H:%M:%S')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger
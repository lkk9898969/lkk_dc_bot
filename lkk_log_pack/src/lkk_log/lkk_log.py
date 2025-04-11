import logging
import warnings
from typing import Literal
from io import StringIO
from pathlib import Path

loglevels = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

warnings.filterwarnings("default", category=DeprecationWarning)


class LkkLogger(logging.Logger):
    def __init__(
        self,
        name: str,
        level: loglevels = "INFO",
        /,
        fileLevel: loglevels = ...,
        filename: str = ...,
        consoleAttach: bool = True,
        fileAttach: bool = True,
        cwd: str | Path = ".",
    ):
        level = matchlevel(level)
        if fileLevel is ...:
            fileLevel = level
        else:
            fileLevel = matchlevel(fileLevel)
        if filename is ...:
            filename = name
        filename = str(Path(cwd) / filename)

        self.name = name
        self.filename = filename
        self.consoleAttach = consoleAttach
        self.fileAttach = fileAttach
        self.level = level
        self.fileLevel = fileLevel
        super().__init__(self.name, logging.DEBUG)
        self.__customInit()

    def __customInit(self):
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s : %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
        )
        self.__stream = StringIO()
        self.__stream_handler = logging.StreamHandler(self.__stream)
        self.__stream_handler.setLevel(logging.DEBUG)
        self.__stream_handler.setFormatter(formatter)
        self.addHandler(self.__stream_handler)
        if self.consoleAttach:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(self.level)
            consoleHandler.setFormatter(formatter)
            self.addHandler(consoleHandler)
        if self.fileAttach:
            fileHandler = logging.FileHandler(self.filename + ".log", encoding="utf-8")
            fileHandler.setLevel(self.fileLevel)
            fileHandler.setFormatter(formatter)
            self.addHandler(fileHandler)

    def debug(
        self,
        msg,
        *args,
        exc_info=None,
        stack_info=False,
        stacklevel=1,
        extra=None,
        console: bool = ...,
    ):
        super().debug(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
        if console is True and self.consoleAttach is False:
            print(self.__stream.getvalue())
        self.__stream.seek(0)
        self.__stream.truncate(0)

    def info(
        self,
        msg,
        *args,
        exc_info=None,
        stack_info=False,
        stacklevel=1,
        extra=None,
        console: bool = ...,
    ):
        super().info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
        if console is True and self.consoleAttach is False:
            print(self.__stream.getvalue())
        self.__stream.seek(0)
        self.__stream.truncate(0)

    def warning(
        self,
        msg,
        *args,
        exc_info=None,
        stack_info=False,
        stacklevel=1,
        extra=None,
        console: bool = ...,
    ):
        super().warning(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
        if console is True and self.consoleAttach is False:
            print(self.__stream.getvalue())
        self.__stream.seek(0)
        self.__stream.truncate(0)

    def error(
        self,
        msg,
        *args,
        exc_info=None,
        stack_info=False,
        stacklevel=1,
        extra=None,
        console: bool = ...,
    ):
        super().error(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
        if console is True and self.consoleAttach is False:
            print(self.__stream.getvalue())
        self.__stream.seek(0)
        self.__stream.truncate(0)

    def critical(
        self,
        msg,
        *args,
        exc_info=None,
        stack_info=False,
        stacklevel=1,
        extra=None,
        console: bool = ...,
    ):
        super().critical(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
        if console is True and self.consoleAttach is False:
            print(self.__stream.getvalue())
        self.__stream.seek(0)
        self.__stream.truncate(0)

    def exception(
        self, msg, *args, exc_info=True, stack_info=False, stacklevel=1, extra=None
    ):
        super().exception(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
        self.__stream.seek(0)
        self.__stream.truncate(0)

    def log(
        self,
        level,
        msg,
        *args,
        exc_info=None,
        stack_info=False,
        stacklevel=1,
        extra=None,
    ):
        super().log(
            level,
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
        self.__stream.seek(0)
        self.__stream.truncate(0)


def loggerhandler(
    loggername: str,
    logfilename: str = ...,
    level: loglevels = "INFO",
    logfile_level: loglevels = ...,
    consoleattach: bool = True,
    logfileattach=True,
    cwd: str | Path = ".",
):
    warnings.warn(
        f"{loggerhandler.__name__} is deprecated, use LkkLogger instead.",
        DeprecationWarning,
    )
    level = matchlevel(level)
    if logfile_level is ...:
        logfile_level = level
    else:
        logfile_level = matchlevel(logfile_level)
    if logfilename is ...:
        logfilename = loggername
    logfilename = str(Path(cwd) / logfilename)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s : %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
    )
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)
    if consoleattach:
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(level)
        consolehandler.setFormatter(formatter)
        logger.addHandler(consolehandler)
    if logfileattach:
        filehandler = logging.FileHandler(logfilename + ".log", encoding="utf-8")
        filehandler.setLevel(logfile_level)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger


def matchlevel(_level: loglevels):
    if type(_level) is str:
        match _level.upper():
            case "DEBUG":
                level = logging.DEBUG
            case "INFO":
                level = logging.INFO
            case "WARNING":
                level = logging.WARNING
            case "ERROR":
                level = logging.ERROR
            case "CRITICAL":
                level = logging.CRITICAL
            case _:
                level = logging.INFO
    elif type(_level) is int:
        if any(
            _level == level
            for level in [
                logging.DEBUG,
                logging.INFO,
                logging.WARNING,
                logging.ERROR,
                logging.CRITICAL,
            ]
        ):
            level = _level
    else:
        level = logging.INFO
    return level

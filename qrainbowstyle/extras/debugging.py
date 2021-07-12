import logging
import traceback

from qtpy.QtCore import QtInfoMsg, QtFatalMsg, QtCriticalMsg, QtWarningMsg


class OutputLogger:
    def __init__(self):
        super(OutputLogger, self).__init__()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.NOTSET)

        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.NOTSET)

        try:
            import coloredlogs
            self.formatter = coloredlogs.ColoredFormatter("%(asctime)s "
                                                          "[%(threadName)s] "
                                                          "[%(name)s] "
                                                          "[%(levelname)s] "
                                                          "%(message)s")
        except ImportError:
            self.formatter = logging.Formatter("%(asctime)s "
                                               "[%(threadName)s] "
                                               "[%(name)s] "
                                               "[%(levelname)s] "
                                               "%(message)s")

        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.info("Logger enabled")

    def set_level(self, level):
        if self.logger and self.handler:
            self.logger.setLevel(level)
            self.handler.setLevel(level)
        else:
            raise Exception("Logger not enabled!")


def qt_message_handler(mode, context, message):
    """Logger for Qt errors"""
    logger = logging.getLogger("QT Logger")
    if mode == QtInfoMsg:
        mode = 20
    elif mode == QtWarningMsg:
        mode = 30
    elif mode == QtCriticalMsg:
        mode = 40
    elif mode == QtFatalMsg:
        mode = 50
    else:
        mode = 20
    logger.log(mode, "(%s: %s): %s" % (context.file, context.line, message))


def catch_exceptions(t, val, tb):
    """Replaces sys.excepthook to catch and log warnings and errors"""
    trace = "".join(traceback.format_exception(t, val, tb))
    logging.getLogger().error(trace)

import logging
import traceback

from qtpy.QtCore import QtInfoMsg, QtFatalMsg, QtCriticalMsg, QtWarningMsg


class OutputLogger:
    """Logging cocfiguration class"""

    def __init__(self):
        super(OutputLogger, self).__init__()
        logging.basicConfig(
            level=logging.NOTSET,
            format="%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()])
        logging.getLogger(self.__class__.__name__).debug("Logger enabled.")


def qt_message_handler(mode, context, message):
    logger = logging.getLogger("QT Logger")
    """Qt errors handler"""
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

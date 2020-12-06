import logging
import traceback

from qtpy.QtCore import QtInfoMsg, QtFatalMsg, QtCriticalMsg, QtWarningMsg

_logger = logging.getLogger(__name__)


class OutputLogger:
    """Logging cocfiguration class"""

    def __init__(self):
        super(OutputLogger, self).__init__()
        logging.basicConfig(
            level=logging.NOTSET,
            format="%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()])
        _logger.debug("Logger enabled.")


def qt_message_handler(mode, context, message):
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
    _logger.log(mode, "%s (%s:%d, %s)" % (message, context.file, context.line, context.file))


def catch_exceptions(t, val, tb):
    """Replaces sys.excepthook to catch and log warnings and errors"""
    trace = "".join(traceback.format_exception(t, val, tb))
    _logger.critical(trace)

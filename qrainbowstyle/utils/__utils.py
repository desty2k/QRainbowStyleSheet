from qtpy import QtCore, QtWidgets

import logging
import traceback

_logger = logging.getLogger(__name__)


def getWorkspace() -> QtCore.QRect:
    """Returns workspace area"""
    return QtWidgets.QApplication.desktop().availableGeometry()


class OutputLogger(object):
    """Logging cocfiguration class"""

    def __init__(self):
        super(OutputLogger, self).__init__()
        logging.basicConfig(
            level=logging.NOTSET,
            format="%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s",
            handlers=[
                logging.StreamHandler()
            ])
        _logger.debug("Logger enabled.")


def qt_message_handler(mode, context, message):
    """Qt errors handler"""
    if mode == QtCore.QtInfoMsg:
        mode = 20
    elif mode == QtCore.QtWarningMsg:
        mode = 30
    elif mode == QtCore.QtCriticalMsg:
        mode = 40
    elif mode == QtCore.QtFatalMsg:
        mode = 50
    else:
        mode = 20
    _logger.log(mode, "%s (%s:%d, %s)" % (message, context.file, context.line, context.file))


def catch_exceptions(t, val, tb):
    """Replaces sys.excepthook to catch and log warnings and errors"""
    trace = "".join(traceback.format_exception(t, val, tb))
    _logger.critical(trace)

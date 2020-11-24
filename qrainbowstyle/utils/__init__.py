#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities for processing SASS and images from default and custom palette.
"""

from qtpy import QtCore, QtWidgets

import sys
import logging
import traceback

_logger = logging.getLogger(__name__)


def getWorkspace() -> QtCore.QRect:
    """Returns workspace area"""
    return QtWidgets.QApplication.desktop().availableGeometry()


class OutputLogger(object):
    """docstring for OutputLogger"""

    def __init__(self):
        super(OutputLogger, self).__init__()
        try:
            if len(open("labnet.log").readlines()) >= 300:
                open("labnet.log", "w").close()
        except Exception:
            pass
        import logging
        logging.basicConfig(
            level=logging.NOTSET,
            format="%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s",
            handlers=[
                logging.StreamHandler()
            ])
        _logger.debug("Logger enabled.")


def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 20
    elif mode == QtCore.QtWarningMsg:
        mode = 30
    elif mode == QtCore.QtCriticalMsg:
        mode = 40
    elif mode == QtCore.QtFatalMsg:
        mode = 50
    else:
        mode = 'Debug'
    _logger.log(mode, "%s (%s:%d, %s)" % (message, context.file, context.line, context.file))


def catch_exceptions(t, val, tb):
    oldhook = sys.excepthook
    trace = "".join(traceback.format_exception(t, val, tb))
    _logger.critical(trace)

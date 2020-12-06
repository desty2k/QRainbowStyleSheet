from qtpy.QtWidgets import QApplication, QDesktopWidget
from qtpy.QtCore import QRect

import qrainbowstyle


def getAllScreensWorkspace() -> list:
    """Returns workspaces of all the available screen.s"""
    return [QDesktopWidget().availableGeometry(x) for x in range(QDesktopWidget().screenCount())]


def getAllScreensGeometry() -> list:
    """Returns geometries of all the available screens."""
    return [QDesktopWidget().screenGeometry(x) for x in range(QDesktopWidget().screenCount())]


def getWorkspace() -> QRect:
    """Returns workspace area of current screen."""
    return QApplication.desktop().availableGeometry()


def setStylesheetOnQApp(style):
    """Set stylesheet on current app."""
    app = QApplication.instance()
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style=style))

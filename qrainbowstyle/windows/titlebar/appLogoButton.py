from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy import QtWidgets, QtGui

import qrainbowstyle


class appLogoButton(QToolButton):

    def __init__(self, parent):
        super(appLogoButton, self).__init__(parent)

        self.setIcon(QtGui.QIcon(qrainbowstyle.APP_ICON_PATH))

        self.setFixedSize(32, 32)
        self.setStyleSheet("border: none;")
        self.setIconSize(QSize(28, 28))
        self.setArrowType(Qt.NoArrow)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)


class appLogoLabel(QLabel):

    def __init__(self, parent):
        super(appLogoLabel, self).__init__(parent)

        self.setPixmap(QtGui.QPixmap(qrainbowstyle.APP_ICON_PATH))
        self.setScaledContents(True)
        self.setFixedSize(25, 25)
        self.setStyleSheet("border: none;")

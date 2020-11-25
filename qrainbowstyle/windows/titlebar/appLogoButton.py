from qtpy.QtWidgets import QToolButton, QLabel
from qtpy.QtGui import QPixmap, QIcon
from qtpy.QtCore import QSize, Qt

import qrainbowstyle


class appLogoButton(QToolButton):

    def __init__(self, parent):
        super(appLogoButton, self).__init__(parent)

        self.setIcon(QIcon(qrainbowstyle.APP_ICON_PATH))

        self.setFixedSize(32, 32)
        self.setStyleSheet("border: none;")
        self.setIconSize(QSize(28, 28))
        self.setArrowType(Qt.NoArrow)
        self.setPopupMode(QToolButton.InstantPopup)


class appLogoLabel(QLabel):

    def __init__(self, parent):
        super(appLogoLabel, self).__init__(parent)

        self.setPixmap(QPixmap(qrainbowstyle.APP_ICON_PATH))
        self.setScaledContents(True)
        self.setFixedSize(25, 25)
        self.setStyleSheet("border: none;")

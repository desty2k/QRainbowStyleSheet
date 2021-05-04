from qtpy.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QToolButton, QLabel, QPushButton
from qtpy.QtGui import QRegion
from qtpy.QtCore import Qt, QSize, QRect

import qrainbowstyle


class MenuButton(QToolButton):
    """MenuButton documentation"""

    def __init__(self, parent):
        super(MenuButton, self).__init__(parent)

        self.setPopupMode(QToolButton.InstantPopup)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)


class AppLogo(QLabel):
    """
        Label with app logo.
    """

    def __init__(self, parent):
        super(AppLogo, self).__init__(parent)
        self.setScaledContents(True)
        self.setFixedSize(QSize(28, 28))
        self.setStyleSheet("border: none;")


class TitlebarWindowsButton(QPushButton):

    def __init__(self, parent):
        super(TitlebarWindowsButton, self).__init__(parent)
        iconsize = QSize(45, 30)
        self.setIconSize(iconsize)
        self.setMinimumSize(iconsize)
        self.setText("")
        self.setEnabled(True)
        self.setAutoFillBackground(True)
        self.setChecked(False)
        self.setMouseTracking(True)

        sizepolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizepolicy)


class MinimizeWindowsButton(TitlebarWindowsButton):

    def __init__(self, parent=None):
        super(MinimizeWindowsButton, self).__init__(parent)


class MaximizeWindowsButton(TitlebarWindowsButton):

    def __init__(self, parent=None):
        super(MaximizeWindowsButton, self).__init__(parent)


class RestoreWindowsButton(TitlebarWindowsButton):

    def __init__(self, parent=None):
        super(RestoreWindowsButton, self).__init__(parent)


class CloseWindowsButton(TitlebarWindowsButton):

    def __init__(self, parent=None):
        super(CloseWindowsButton, self).__init__(parent)


class CloseSquareWindowsButton(TitlebarWindowsButton):

    def __init__(self, parent=None):
        super(CloseSquareWindowsButton, self).__init__(parent)
        iconsize = QSize(30, 30)
        self.setIconSize(iconsize)
        self.setMinimumSize(iconsize)


class TitlebarDarwinButton(QPushButton):

    def __init__(self, parent):
        super(TitlebarDarwinButton, self).__init__(parent)
        self.setIconSize(QSize(15, 15))
        self.setMinimumSize(QSize(15, 15))
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        sizepolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizepolicy)


class MinimizeDarwinButton(TitlebarDarwinButton):

    def __init__(self, parent=None):
        super(MinimizeDarwinButton, self).__init__(parent)


class MaximizeDarwinButton(TitlebarDarwinButton):

    def __init__(self, parent=None):
        super(MaximizeDarwinButton, self).__init__(parent)


class RestoreDarwinButton(TitlebarDarwinButton):

    def __init__(self, parent=None):
        super(RestoreDarwinButton, self).__init__(parent)


class CloseDarwinButton(TitlebarDarwinButton):

    def __init__(self, parent=None):
        super(CloseDarwinButton, self).__init__(parent)


class ButtonsWidget(QWidget):
    """Widget with titlebar buttons"""

    def __init__(self, parent):
        super(ButtonsWidget, self).__init__(parent)
        self.setObjectName("buttonsWidget")
        self.setContentsMargins(0, 0, 0, 0)
        sizepolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizepolicy)
        self.setStyleSheet("padding: 0px;")

        self.buttonsLayout = QHBoxLayout(self)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setSpacing(0)
        self.buttonsLayout.setAlignment(Qt.AlignVCenter)
        self.setLayout(self.buttonsLayout)
        if qrainbowstyle.USE_DARWIN_BUTTONS:
            self.btnMinimize = MinimizeDarwinButton(self)
            self.btnMaximize = MaximizeDarwinButton(self)
            self.btnRestore = RestoreDarwinButton(self)
            self.btnClose = CloseDarwinButton(self)
        else:
            self.btnMinimize = MinimizeWindowsButton(self)
            self.btnMaximize = MaximizeWindowsButton(self)
            self.btnRestore = RestoreWindowsButton(self)
            self.btnClose = CloseWindowsButton(self)

        if qrainbowstyle.ALIGN_BUTTONS_LEFT:
            self.buttonsLayout.addWidget(self.btnClose)
            if not qrainbowstyle.USE_DARWIN_BUTTONS:
                self.buttonsLayout.addWidget(self.btnRestore)
            self.buttonsLayout.addWidget(self.btnMinimize)
            self.buttonsLayout.addWidget(self.btnMaximize)
        else:
            self.buttonsLayout.addWidget(self.btnMinimize)
            self.buttonsLayout.addWidget(self.btnMaximize)
            if not qrainbowstyle.USE_DARWIN_BUTTONS:
                self.buttonsLayout.addWidget(self.btnRestore)
            self.buttonsLayout.addWidget(self.btnClose)

        self.btnMinimize.setObjectName("btnMinimize")
        self.btnMaximize.setObjectName("btnMaximize")
        if not qrainbowstyle.USE_DARWIN_BUTTONS:
            self.btnRestore.setObjectName("btnRestore")
        self.btnClose.setObjectName("btnClose")

        if qrainbowstyle.USE_DARWIN_BUTTONS:
            self.buttonsLayout.setSpacing(8)

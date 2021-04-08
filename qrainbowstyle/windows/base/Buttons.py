from qtpy.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QToolButton, QLabel
from qtpy.QtGui import QIcon, QRegion
from qtpy.QtCore import Qt, QEvent, QSize, QRect

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
        self.setFixedSize(QSize(32, 32))
        self.setStyleSheet("border: none;")


class DarwinButton(QToolButton):

    def __init__(self, icon: QIcon, hovericon: QIcon, parent=None):
        super(DarwinButton, self).__init__(parent)

        self.setMask(QRegion(QRect(0, 0, 15, 15), QRegion.Ellipse))
        self.setMinimumSize(QSize(14, 14))
        self.setIconSize(QSize(14, 14))
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)

        self.icon = icon
        self.hoverIcon = hovericon

        self.setIcon(self.icon)

    def enterEvent(self, event: QEvent) -> None:
        self.setIcon(self.hoverIcon)

    def leaveEvent(self, event: QEvent) -> None:
        self.setIcon(self.icon)

    def setIcons(self, normal: QIcon, hover: QIcon):
        self.icon = normal
        self.hoverIcon = hover


class WindowsButton(QToolButton):

    def __init__(self, icon: QIcon = None, hovericon: QIcon = None, parent=None):
        super(WindowsButton, self).__init__(parent)

        if not icon:
            raise Exception("Icon is required")

        self.icon = icon
        self.hoverIcon = hovericon

        iconsize = QSize(45, 30)
        self.setText("")
        self.setEnabled(True)
        self.setIconSize(iconsize)
        self.setMinimumSize(iconsize)
        self.setAutoFillBackground(True)
        self.setChecked(False)
        self.setMouseTracking(True)

        self.setIcon(self.icon)

        sizepolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizepolicy)

    def setIcons(self, normal: QIcon, hover: QIcon):
        self.icon = normal
        self.hoverIcon = hover

    def enterEvent(self, event: QEvent) -> None:
        if self.hoverIcon:
            self.setIcon(self.hoverIcon)

    def leaveEvent(self, event: QEvent) -> None:
        self.setIcon(self.icon)


class ButtonsWidget(QWidget):
    """Widget with titlebar buttons"""

    def __init__(self, parent):
        super(ButtonsWidget, self).__init__(parent)

        self.setObjectName("buttonsWidget")
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
            self.btnMinimize = DarwinButton(QIcon(":/qss_icons/rc/button_darwin_minimize.png"),
                                            QIcon(":/qss_icons/rc/button_darwin_minimize_hover.png"),
                                            self)
            self.btnMaximize = DarwinButton(QIcon(":/qss_icons/rc/button_darwin_maximize.png"),
                                            QIcon(":/qss_icons/rc/button_darwin_maximize_hover.png"),
                                            self)
            self.btnRestore = DarwinButton(QIcon(":/qss_icons/rc/button_darwin_restore.png"),
                                           QIcon(":/qss_icons/rc/button_darwin_restore_hover.png"),
                                           self)
            self.btnClose = DarwinButton(QIcon(":/qss_icons/rc/button_darwin_close.png"),
                                         QIcon(":/qss_icons/rc/button_darwin_close_hover.png"),
                                         self)

        else:
            self.btnMinimize = WindowsButton(QIcon(":/qss_icons/rc/button_nt_minimize.png"),
                                             QIcon(":/qss_icons/rc/button_nt_minimize_hover.png"),
                                             self)
            self.btnMaximize = WindowsButton(QIcon(":/qss_icons/rc/button_nt_maximize.png"),
                                             QIcon(":/qss_icons/rc/button_nt_maximize_hover.png"),
                                             self)
            self.btnRestore = WindowsButton(QIcon(":/qss_icons/rc/button_nt_restore.png"),
                                            QIcon(":/qss_icons/rc/button_nt_restore_hover.png"),
                                            self)
            self.btnClose = WindowsButton(QIcon(":/qss_icons/rc/button_nt_close.png"),
                                          QIcon(":/qss_icons/rc/button_nt_close_hover_red.png"),
                                          self)

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

    def updateButtons(self):
        if qrainbowstyle.USE_DARWIN_BUTTONS:
            self.btnMinimize.setIcons(QIcon(":/qss_icons/rc/button_darwin_minimize.png"),
                                      QIcon(":/qss_icons/rc/button_darwin_minimize_hover.png"))

            self.btnMaximize.setIcons(QIcon(":/qss_icons/rc/button_darwin_maximize.png"),
                                      QIcon(":/qss_icons/rc/button_darwin_maximize_hover.png"))
            self.btnRestore.setIcons(QIcon(":/qss_icons/rc/button_darwin_restore_hover.png"),
                                     QIcon(":/qss_icons/rc/button_darwin_restore_hover.png"))
            self.btnClose.setIcons(QIcon(":/qss_icons/rc/button_darwin_close.png"),
                                   QIcon(":/qss_icons/rc/button_darwin_close_hover.png"))

        else:
            self.btnMinimize.setIcons(QIcon(":/qss_icons/rc/button_nt_minimize.png"),
                                      QIcon(":/qss_icons/rc/button_nt_minimize_hover.png"))
            self.btnMaximize.setIcons(QIcon(":/qss_icons/rc/button_nt_maximize.png"),
                                      QIcon(":/qss_icons/rc/button_nt_maximize_hover.png"))
            self.btnRestore.setIcons(QIcon(":/qss_icons/rc/button_nt_restore.png"),
                                     QIcon(":/qss_icons/rc/button_nt_restore_hover.png"))
            self.btnClose.setIcons(QIcon(":/qss_icons/rc/button_nt_close.png"),
                                   QIcon(":/qss_icons/rc/button_nt_close_hover_red.png"))

        self.btnMinimize.leaveEvent(None)
        self.btnMaximize.leaveEvent(None)
        self.btnRestore.leaveEvent(None)
        self.btnClose.leaveEvent(None)

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.StyleChange:
            if (hasattr(self, "btnMinimize")
                    and hasattr(self, "btnMaximize")
                    and hasattr(self, "btnRestore")
                    and hasattr(self, "btnClose")):
                self.updateButtons()

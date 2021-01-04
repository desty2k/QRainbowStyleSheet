from qtpy.QtWidgets import QToolButton, QSizePolicy
from qtpy.QtGui import QRegion, QIcon
from qtpy.QtCore import QRect, QSize, QEvent


class titleBarButton(QToolButton):

    def __init__(self, icon: QIcon, hovericon: QIcon, parent=None):
        super(titleBarButton, self).__init__(parent)

        self.setMask(QRegion(QRect(0, 0, 21, 21), QRegion.Ellipse))
        self.setMinimumSize(20, 20)
        self.setIconSize(QSize(20, 20))
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


class titleBarWindowsButton(QToolButton):

    def __init__(self, icon: QIcon = None, hovericon: QIcon = None, parent=None):
        super(titleBarWindowsButton, self).__init__(parent)

        if not icon:
            raise Exception("Icon is required")

        self.icon = icon
        self.hoverIcon = hovericon

        # iconsize = self.icon.availableSizes()[0]
        iconsize = QSize(45, 30)
        self.setEnabled(True)
        self.setMinimumSize(iconsize)
        self.setAutoFillBackground(True)
        self.setText("")
        self.setIconSize(iconsize)
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

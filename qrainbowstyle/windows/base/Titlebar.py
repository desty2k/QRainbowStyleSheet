from qtpy.QtWidgets import QFrame, QMenu, QHBoxLayout, QLabel, QSizePolicy
from qtpy.QtCore import Signal, QPoint, QMetaObject, Slot, Qt, QRect
from qtpy.QtGui import QPalette, QPixmap, QIcon

from .Buttons import ButtonsWidget, AppLogo, MenuButton

import qrainbowstyle


class Titlebar(QFrame):
    """Titlebar for frameless windows."""

    minimizeClicked = Signal()
    maximizeClicked = Signal()
    restoreClicked = Signal()
    closeClicked = Signal()

    def __init__(self, parent=None):
        super(Titlebar, self).__init__(parent)
        self.setObjectName("titlebar")
        self.setMouseTracking(True)

        self.menus = []

        self.setAutoFillBackground(True)
        self.setFixedHeight(30)
        self.setContentsMargins(0, 0, 0, 0)
        self.setBackgroundRole(QPalette.Highlight)

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setContentsMargins(8, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.appLogoLabel = AppLogo(self)
        if qrainbowstyle.APP_ICON_PATH:
            self.appLogoLabel.setPixmap(QPixmap(qrainbowstyle.APP_ICON_PATH))
            self.layout.setContentsMargins(2, 0, 0, 0)
        self.layout.addWidget(self.appLogoLabel)
        if qrainbowstyle.ALIGN_BUTTONS_LEFT:
            self.appLogoLabel.setVisible(False)
            self.layout.setContentsMargins(8, 0, 0, 0)

        self.layout.insertStretch(50)
        self.buttonsWidget = ButtonsWidget(self)
        if qrainbowstyle.ALIGN_BUTTONS_LEFT:
            self.layout.insertWidget(0, self.buttonsWidget)
        else:
            self.layout.addWidget(self.buttonsWidget)

        # auto connect signals
        QMetaObject.connectSlotsByName(self)
        if self.window().parent() is not None:
            self.buttonsWidget.btnRestore.setVisible(False)
            self.buttonsWidget.btnMaximize.setVisible(False)
            self.buttonsWidget.btnMinimize.setVisible(False)

    def setWindowIcon(self, icon: QIcon):
        self.appLogoLabel.setPixmap(icon.pixmap())

    # connecting buttons signals
    @Slot()
    def on_btnClose_clicked(self):
        self.closeClicked.emit()

    @Slot()
    def on_btnRestore_clicked(self):
        self.showRestoreButton(False)
        self.showMaximizeButton(True)
        self.window().showNormal()
        self.restoreClicked.emit()

    @Slot()
    def on_btnMaximize_clicked(self):
        if qrainbowstyle.USE_DARWIN_BUTTONS:
            if self.window().isMaximized():
                self.window().showNormal()
            else:
                self.window().showMaximized()
        else:
            self.showRestoreButton(True)
            self.showMaximizeButton(False)
            self.window().showMaximized()
        self.maximizeClicked.emit()

    @Slot()
    def on_btnMinimize_clicked(self):
        self.window().showMinimized()

    def showLogo(self, value: bool):
        """Show or hide app logo label"""
        self.appLogoLabel.setVisible(value)

    def showRestoreButton(self, value):
        if self.window().parent() is None:
            self.buttonsWidget.btnRestore.setVisible(value)

    def showMaximizeButton(self, value):
        if self.window().parent() is None:
            self.buttonsWidget.btnMaximize.setVisible(value)

    def showMinimizeButton(self, value):
        if self.window().parent() is None:
            self.buttonsWidget.btnMinimize.setVisible(value)

    def addMenu(self, menu: QMenu):
        menuButton = MenuButton(self)
        menuButton.setMenu(menu)
        menuButton.setText(menu.title())
        self.layout.insertWidget(len(self.menus) + 1, menuButton)
        self.menus.append(menuButton)

    def setTitlebarHeight(self, height: int):
        self.setFixedHeight(height)

    def mouseOverTitlebar(self, x, y):
        if self.childAt(QPoint(x, y)):
            return False
        else:
            return QRect(self.appLogoLabel.width(), 0,
                         self.width() - self.appLogoLabel.width(),
                         self.height()).contains(QPoint(x, y))

from qtpy.QtWidgets import QApplication, QFrame, QMenu, QLabel, QHBoxLayout, QWidget
from qtpy.QtCore import Signal, QPoint, QMetaObject, Slot, Qt
from qtpy.QtGui import QPalette

from .appLogoButton import appLogoLabel, appLogoButton
from .buttonsWidget import buttonsWidget

import qrainbowstyle
from qrainbowstyle.utils import getWorkspace


class Titlebar(QFrame):
    """Titlebar for frameless windows."""

    minimizeClicked = Signal()
    maximizeClicked = Signal()
    restoreClicked = Signal()
    closeClicked = Signal()

    def __init__(self, parentwindow: QWidget, parent=None):
        super(Titlebar, self).__init__(parent)
        self.setObjectName("titlebar")

        self.window = parentwindow
        self.offset = QPoint()
        self.maxNormal = False
        self.moving = False
        self._maximizeondbclick = True
        self._enablesnapping = True

        self.setAutoFillBackground(True)
        self.setFixedHeight(45)
        self.setContentsMargins(0, 0, 0, 0)
        self.setBackgroundRole(QPalette.Highlight)

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.setLayout(self.layout)

        self.appLogoLabel = appLogoLabel(self)
        self.layout.addWidget(self.appLogoLabel)

        self.appLogoButton = appLogoButton(self)
        self.layout.addWidget(self.appLogoButton)

        self.label = QLabel(self)
        self.label.setText(qrainbowstyle.APP_NAME)
        self.label.setAlignment(Qt.AlignVCenter)
        self.label.mouseMoveEvent = self.mouseMoveEvent
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseReleaseEvent = self.mouseReleaseEvent
        self.layout.addWidget(self.label)
        if qrainbowstyle.ALIGN_BUTTONS_LEFT:
            self.layout.setAlignment(self.label, Qt.AlignCenter)

        self.layout.insertStretch(3)

        self.buttonsWidget = buttonsWidget(self)

        if qrainbowstyle.ALIGN_BUTTONS_LEFT:
            self.layout.insertWidget(0, self.buttonsWidget)
        else:
            self.layout.addWidget(self.buttonsWidget)

        # auto connect signals
        QMetaObject.connectSlotsByName(self)

    # connecting buttons signals
    @Slot()
    def on_btnClose_clicked(self):
        self.closeClicked.emit()

    @Slot()
    def on_btnRestore_clicked(self):
        self.showRestoreButton(False)
        self.showMaximizeButton(True)
        self.window.setWindowState(Qt.WindowNoState)
        self.maxNormal = False
        self.restoreClicked.emit()

    @Slot()
    def on_btnMaximize_clicked(self):
        if qrainbowstyle.USE_DARWIN_BUTTONS:
            if self.window.windowState() == Qt.WindowMaximized:
                self.window.setWindowState(Qt.WindowNoState)
                self.maxNormal = False
            else:
                self.window.setWindowState(Qt.WindowMaximized)
                self.maxNormal = True
        else:
            self.showRestoreButton(True)
            self.showMaximizeButton(False)
            self.window.setWindowState(Qt.WindowMaximized)
            self.maxNormal = True
        self.maximizeClicked.emit()

    @Slot()
    def on_btnMinimize_clicked(self):
        self.window.showMinimized()
        self.minimizeClicked.emit()

    def maximizeOnDoubleClick(self, value: bool):
        """Enable or disable maximize on double click."""
        self._maximizeondbclick = value

    def enableEdgesSnapping(self, value: bool):
        """Enable snapping to edges."""
        self._enablesnapping = value

    def setWindowTitle(self, title: str) -> None:
        """Set window title"""
        self.label.setText(title)

    def showLogoLabel(self, value: bool):
        """Show or hide app logo label"""
        self.appLogoLabel.setVisible(value)

    def showLogoButton(self, value: bool):
        """Show or hide menu button with app logo button"""
        self.appLogoButton.setVisible(value)

    def showRestoreButton(self, value):
        self.buttonsWidget.btnRestore.setVisible(value)

    def showMaximizeButton(self, value):
        self.buttonsWidget.btnMaximize.setVisible(value)

    def showMinimizeButton(self, value):
        self.buttonsWidget.btnMinimize.setVisible(value)

    def setMenu(self, menu: QMenu):
        """Set app logo button menu"""
        self.appLogoButton.setMenu(menu)

    def setTitlebarHeight(self, height: int):
        self.setFixedHeight(height)

    def showMaxRestore(self):
        """btnMaximize if normal, restore if btnMaximized"""
        if self.maxNormal:
            self.showRestoreButton(False)
            self.showMaximizeButton(True)
            self.window.setWindowState(Qt.WindowNoState)
            self.maxNormal = False

        else:
            self.showRestoreButton(True)
            self.showMaximizeButton(False)
            self.window.setWindowState(Qt.WindowMaximized)
            self.maxNormal = True

    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.LeftButton:
            self.moving = True
            if self.label.underMouse():
                self.offset = event.pos() + self.pos() + self.label.pos()
            else:
                self.offset = event.pos() + self.pos()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events"""
        if self.moving and self._enablesnapping:
            screen = QApplication.desktop().availableGeometry()

            if event.globalY() == 0:
                self.on_btnMaximize_clicked()

            elif event.globalX() == 0:
                self.window.move(0, 0)
                self.window.resize(screen.width() / 2, screen.height())
                self.window.setWindowState(Qt.WindowNoState)
                self.maxNormal = False

            elif event.globalX() + 1 >= screen.width():
                self.window.move(screen.width() / 2, 0)
                self.window.resize(screen.width() / 2, screen.height())
                self.window.setWindowState(Qt.WindowNoState)
                self.maxNormal = False

        self.moving = False

    def mouseDoubleClickEvent(self, event):
        if self._maximizeondbclick:
            self.showMaxRestore()

    def mouseMoveEvent(self, event):
        """Handle mouse moving"""
        if self.maxNormal:
            workarea = getWorkspace()
            self.moving = False
            self.on_btnRestore_clicked()
            self.window.resize(workarea.width(), workarea.height())
            self.moving = True

        if self.moving:
            if not self.buttonsWidget.underMouse():
                self.window.move(event.globalPos() - self.offset)

    def resizeEvent(self, event):
        """Handle resizing events"""
        self.buttonsWidget.btnMaximize.leaveEvent(None)
        if not qrainbowstyle.USE_DARWIN_BUTTONS:
            self.buttonsWidget.btnRestore.leaveEvent(None)

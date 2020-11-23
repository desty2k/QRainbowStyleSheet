from .appLogoButton import *
from .buttonsWidget import *


def getWorkspace() -> QtCore.QRect:
    """Returns workspace area"""
    return QtWidgets.QApplication.desktop().availableGeometry()


class Titlebar(QFrame):
    minimizeClicked = Signal()
    maximizeClicked = Signal()
    restoreClicked = Signal()
    closeClicked = Signal()
    """Titlebar documentation"""

    def __init__(self, parentwindow: QWidget, parent=None):
        super(Titlebar, self).__init__(parent)
        self.setObjectName("titlebar")

        self.window = parentwindow
        self.offset = QPoint()
        self.maxNormal = False
        self.moving = False

        self.setAutoFillBackground(True)
        self.setFixedHeight(45)
        self.setContentsMargins(0, 0, 0, 0)
        self.setBackgroundRole(QtGui.QPalette.Highlight)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.setLayout(self.layout)

        self.appLogoLabel = appLogoLabel(self)
        self.layout.addWidget(self.appLogoLabel)

        self.appLogoButton = appLogoButton(self)
        self.layout.addWidget(self.appLogoButton)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(qdarkstyle.APP_NAME)
        self.label.setAlignment(Qt.AlignVCenter)
        self.label.mouseMoveEvent = self.mouseMoveEvent
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseReleaseEvent = self.mouseReleaseEvent
        self.layout.addWidget(self.label)
        if qdarkstyle.ALIGN_BUTTONS_LEFT:
            self.layout.setAlignment(self.label, Qt.AlignCenter)

        self.layout.insertStretch(3)

        self.buttonsWidget = buttonsWidget(self)

        if qdarkstyle.ALIGN_BUTTONS_LEFT:
            self.layout.insertWidget(0, self.buttonsWidget)
        else:
            self.layout.addWidget(self.buttonsWidget)

        # auto connect signals
        QMetaObject.connectSlotsByName(self)

    # connecting buttons signals
    @Slot()
    def on_btnClose_clicked(self):
        self.window.close()
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
        if qdarkstyle.USE_DARWIN_BUTTONS:
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
        if not qdarkstyle.USE_DARWIN_BUTTONS:
            self.buttonsWidget.btnRestore.setVisible(value)

    def showMaximizeButton(self, value):
        if not qdarkstyle.USE_DARWIN_BUTTONS:
            self.buttonsWidget.btnMaximize.setVisible(value)

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
        if self.moving:
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
        if not qdarkstyle.USE_DARWIN_BUTTONS:
            self.buttonsWidget.btnRestore.leaveEvent(None)

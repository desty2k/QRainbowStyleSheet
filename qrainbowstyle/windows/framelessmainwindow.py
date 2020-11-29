from qtpy.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QSizePolicy, QSizeGrip, QMenu
from qtpy.QtGui import QMouseEvent
from qtpy.QtCore import Qt, QMetaObject, QTimer, Slot

from .titlebar import Titlebar


class FramelessMainWindow(QMainWindow):
    """
    Frameless main window
    Args:
        parent (QWidget, optional): Parent widget.
    """

    def __init__(self, parent=None):
        super(FramelessMainWindow, self).__init__(parent)

        self._contentWidgets = []

        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowCloseButtonHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        # For preview
        screen = QApplication.desktop().availableGeometry()
        self.resize(screen.width() / 2, screen.height() / 2)
        self.setContentsMargins(0, 0, 0, 0)

        self._centralWidget = QWidget(self)
        self._centralWidget.setObjectName("centralWidget")
        self._centralWidget.setContentsMargins(0, 0, 0, 0)

        self._centralLayout = QVBoxLayout(self._centralWidget)
        self._centralLayout.setAlignment(Qt.AlignBottom)
        self._centralLayout.setSpacing(3)
        self._centralLayout.setContentsMargins(5, 5, 5, 5)

        self._bar = Titlebar(self)
        self._bar.showRestoreButton(False)
        self._bar.showLogoLabel(False)
        self._bar.showLogoButton(True)
        self._centralLayout.addWidget(self._bar)
        self._centralLayout.setAlignment(self._bar, Qt.AlignVCenter)

        self._centralLayout.addSpacing(3)

        self._contentWidget = QWidget(self)
        self._contentWidget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding)
        self._contentWidgetLayout = QVBoxLayout(self._contentWidget)
        self._contentWidgetLayout.setContentsMargins(6, 6, 6, 6)
        self._centralLayout.addWidget(self._contentWidget)

        self._sizegrip = QSizeGrip(self._centralWidget)
        self._centralLayout.addWidget(self._sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        self._centralWidget.setLayout(self._centralLayout)
        self.setCentralWidget(self._centralWidget)

        self._fullscreenTitlebarTimer = QTimer(self)
        self._fullscreenTitlebarTimer.setObjectName("_fullscreenTitlebarTimer")

        self._contentWidget.setAutoFillBackground(True)

        self.minimizeClicked = self._bar.minimizeClicked
        self.maximizeClicked = self._bar.maximizeClicked
        self.restoreClicked = self._bar.restoreClicked
        self.closeClicked = self._bar.closeClicked

        QMetaObject.connectSlotsByName(self)

    def showSizeGrip(self, value: bool):
        """Show or hide size grip.

        Args:
            value (bool): To show or to hide.
        """
        self._sizegrip.setVisible(value)

    def setMenu(self, menu: QMenu):
        """Set menu for app icon.

        Args:
            menu (QMenu): QMenu to show.
        """
        self._bar.setMenu(menu)

    def setTitlebarHeight(self, height: int):
        """Set titlebar height.

        Args:
            height (int): Titlebar height.
        """
        self._bar.setTitlebarHeight(height)

    def addContentWidget(self, widget: QWidget):
        """Add master widget to window.

        Args:
            widget (QWidget): Content widget.
        """
        self._contentWidgets.append(widget)
        self._contentWidgetLayout.addWidget(widget)

    def insertContentWidget(self, index, widget: QWidget):
        """Insert master widget to window at pos.

        Args:
            index (int): Index
            widget (QWidget): Content widget.
        """
        self._contentWidgets.insert(index, widget)
        self._contentWidgetLayout.insertWidget(index, widget)

    def showFullScreen(self) -> None:
        """Show app in fullscreen mode"""
        self.setWindowState(Qt.WindowFullScreen)

        firstshow_timer = QTimer(self)
        firstshow_timer.timeout.connect(self._on_showFullScreen)
        firstshow_timer.start(3000)

    def _on_showFullScreen(self):
        if self.windowState() == Qt.WindowFullScreen:
            self._bar.setVisible(False)
            self._separator.setVisible(False)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press events

        Args:
            index (QMouseEvent): Mouse press event
        """
        if self.windowState() == Qt.WindowFullScreen:
            ypos = event.globalY()
            if ypos <= 5:
                self._bar.setVisible(True)
                self._separator.setVisible(True)
                self._fullscreenTitlebarTimer.start(2500)
        else:
            self._fullscreenTitlebarTimer.stop()

    @Slot()
    def on__fullscreenTitlebarTimer_timeout(self):
        if self.windowState() == Qt.WindowFullScreen:
            self._bar.setVisible(False)
            self._separator.setVisible(False)

from qtpy.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QSizePolicy, QMenu
from qtpy.QtGui import QMouseEvent, QResizeEvent, QIcon
from qtpy.QtCore import Qt, QMetaObject, QTimer, Slot, QEvent, QObject

from .titlebar import Titlebar
from .titlebar.resizer import Resizer


class FramelessMainWindow(QMainWindow):
    """Frameless main window.

    Args:
        parent (QWidget, optional): Parent widget.
    """

    def __init__(self, parent=None):
        super(FramelessMainWindow, self).__init__(parent)
        self._contentWidgets = []
        self._enableResizing = True

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        # For preview
        screen = QApplication.desktop().availableGeometry()
        self.resize(screen.width() / 2, screen.height() / 2)
        self.setContentsMargins(0, 0, 0, 0)

        self._centralWidget = QWidget(self)
        self._centralWidget.setObjectName("centralWidget")
        self._centralWidget.setContentsMargins(2.5, 2.5, 2.5, 2.5)
        self._centralWidget.setMouseTracking(True)

        self._centralLayout = QVBoxLayout(self._centralWidget)
        self._centralLayout.setAlignment(Qt.AlignBottom)
        self._centralLayout.setSpacing(3)
        self._centralLayout.setContentsMargins(0, 0, 0, 0)

        self._bar = Titlebar(self)
        self._bar.showRestoreButton(False)
        self._bar.showLogoLabel(False)
        self._bar.showLogoButton(True)
        self._bar.closeClicked.connect(self.close)
        self._centralLayout.addWidget(self._bar)
        self._centralLayout.setAlignment(self._bar, Qt.AlignVCenter)

        self._centralLayout.addSpacing(3)

        self._contentWidget = QWidget(self)
        self._contentWidget.setMouseTracking(True)
        self._contentWidget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding)
        self._contentWidget.setContentsMargins(0, 0, 0, 0)
        self._contentWidgetLayout = QVBoxLayout(self._contentWidget)
        self._contentWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self._centralLayout.addWidget(self._contentWidget)

        self._centralWidget.setLayout(self._centralLayout)
        self.setCentralWidget(self._centralWidget)

        self._fullscreenTitlebarTimer = QTimer(self)
        self._fullscreenTitlebarTimer.setObjectName("_fullscreenTitlebarTimer")

        self._contentWidget.setAutoFillBackground(True)

        self.minimizeClicked = self._bar.minimizeClicked
        self.maximizeClicked = self._bar.maximizeClicked
        self.restoreClicked = self._bar.restoreClicked
        self.closeClicked = self._bar.closeClicked

        # create resizer
        self.resizehandler = Resizer(self, debug=False)
        self.resizehandler.updateTitlebarHeight(self._bar.height())
        QApplication.instance().installEventFilter(self)

        QMetaObject.connectSlotsByName(self)

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
        self.resizehandler.updateTitlebarHeight(self._bar.height())

    def setWindowTitle(self, title: str) -> None:
        self._bar.setWindowTitle(title)
        super().setWindowTitle(title)

    def setWindowIcon(self, icon: QIcon) -> None:
        self._bar.setWindowIcon(icon)
        super().setWindowIcon(icon)

    def eventFilter(self, source, event):
        """Handles events. When in full screen mode the user places
        the cursor no more than five pixels from the top of the screen,
        a bar with buttons will appear. When the window is in NoState,
        the user is able to resize the window by hovering
        the cursor over the lower right corner of the window.

        Args:
            source (QObject): Event source.
            event (QEvent): Event.
        """

        # fullscreen hover to show buttons
        if self.windowState() == Qt.WindowFullScreen:
            if event.type() == QMouseEvent.MouseMove:
                ypos = event.globalY()
                if ypos <= 5:
                    self._bar.setVisible(True)
                    self._fullscreenTitlebarTimer.start(2500)
            else:
                self._fullscreenTitlebarTimer.stop()

        if hasattr(self, "resizehandler"):
            self.resizehandler.handle(source, event, self)
        return super().eventFilter(source, event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events

        Args:
            event (QResizeEvent): Resize event
        """
        pass

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

    def setResizingEnabled(self, value: bool):
        """Enable window resizing

        Args:
            value (bool): Enable or disable window resizing
        """
        self._enableResizing = value

    def isResizingEnabled(self) -> bool:
        """Return if window allows resizing

        Returns:
            value (bool): Window allow resizing.
        """
        return self._enableResizing

    def _on_showFullScreen(self):
        if self.windowState() == Qt.WindowFullScreen:
            self._bar.setVisible(False)

    @Slot()
    def on__fullscreenTitlebarTimer_timeout(self):
        if self.windowState() == Qt.WindowFullScreen:
            self._bar.setVisible(False)

from qtpy.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QSizePolicy, QMenu
from qtpy.QtGui import QMouseEvent, QResizeEvent
from qtpy.QtCore import Qt, QMetaObject, QTimer, Slot, QRect, QPoint, QEvent

from .titlebar import Titlebar


class FramelessMainWindow(QMainWindow):
    """Frameless main window.

    Args:
        parent (QWidget, optional): Parent widget.
    """

    def __init__(self, parent=None):
        super(FramelessMainWindow, self).__init__(parent)
        self._contentWidgets = []

        self._gripsize = 5
        self._dndetect = QPoint(0, 0)
        self._griprect = QRect(self.width() - self._gripsize,
                               self.height() - self._gripsize,
                               self._gripsize - self._dndetect.x(),
                               self._gripsize - self._dndetect.y())
        self._resizing = False

        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowCloseButtonHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

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

        QApplication.instance().installEventFilter(self)

    def _updateGripRect(self):
        self._griprect = QRect(self.width() - self._gripsize,
                               self.height() - self._gripsize,
                               self._gripsize - self._dndetect.x(),
                               self._gripsize - self._dndetect.y())

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

    def eventFilter(self, source, event):
        """Handles events. When in full screen mode the user places
        the cursor no more than five pixels from the top of the screen,
        a bar with buttons will appear. When the window is in NoState,
        the user will be able to change the window size by hovering
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

        # resizing
        if self.windowState() not in (Qt.WindowFullScreen, Qt.WindowMaximized):
            if event.type() == QMouseEvent.MouseButtonPress:
                self._updateGripRect()
                if self._griprect.contains(event.pos()):
                    self._resizing = True

            if event.type() == QMouseEvent.MouseButtonRelease:
                QApplication.restoreOverrideCursor()
                self._resizing = False

            if event.type() == QMouseEvent.MouseMove:
                self._updateGripRect()
                if self._resizing:
                    QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
                    if event.buttons() == Qt.LeftButton:
                        self.resize(event.x(), event.y())
                        self._updateGripRect()
                        self.update()
                        QApplication.restoreOverrideCursor()
                else:
                    if self._griprect.contains(event.pos()):
                        QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
                    else:
                        QApplication.restoreOverrideCursor()

        return QMainWindow.eventFilter(self, source, event)

    def resizeEvent(self, a0: QResizeEvent) -> None:
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

    def _on_showFullScreen(self):
        if self.windowState() == Qt.WindowFullScreen:
            self._bar.setVisible(False)

    @Slot()
    def on__fullscreenTitlebarTimer_timeout(self):
        if self.windowState() == Qt.WindowFullScreen:
            self._bar.setVisible(False)

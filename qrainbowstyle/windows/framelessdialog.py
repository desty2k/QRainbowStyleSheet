from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy, QDialog
from qtpy.QtGui import QResizeEvent, QMouseEvent, QIcon
from qtpy.QtCore import Qt, QMetaObject, QEvent

from .titlebar import Titlebar
from .titlebar.resizer import Resizer


class FramelessDialog(QDialog):
    """FramelessDialog documentation"""

    def __init__(self, parent=None):
        super(FramelessDialog, self).__init__(parent)
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
        self._bar.showMinimizeButton(False)
        self._bar.showMaximizeButton(False)
        self._bar.showLogoLabel(True)
        self._bar.showLogoButton(False)
        self._bar.maximizeOnDoubleClick(False)
        self._bar.enableEdgesSnapping(False)
        self._bar.closeClicked.connect(self.close)
        self._centralLayout.addWidget(self._bar)
        self._centralLayout.setAlignment(self._bar, Qt.AlignVCenter)

        self._centralLayout.addSpacing(3)

        self._contentWidget = QWidget(self)
        self._contentWidget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding)
        self._contentWidget.setContentsMargins(0, 0, 0, 0)
        self._contentWidgetLayout = QVBoxLayout(self._contentWidget)
        self._contentWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self._centralLayout.addWidget(self._contentWidget)

        self._centralWidget.setLayout(self._centralLayout)
        self._contentWidget.setAutoFillBackground(True)

        self.minimizeClicked = self._bar.minimizeClicked
        self.closeClicked = self._bar.closeClicked

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        self._layout.addWidget(self._centralWidget)

        # create resizer
        self.resizehandler = Resizer(debug=False)
        self.resizehandler.updateTitlebarHeight(self._bar.height())
        QApplication.instance().installEventFilter(self)

        QMetaObject.connectSlotsByName(self)

    def setTitlebarHeight(self, height: int):
        """Set titlebar height.

        Args:
            height (int): Titlebar height.
        """
        self._bar.setTitlebarHeight(height)

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

        if hasattr(self, "resizehandler"):
            self.resizehandler.handle(source, event, self)
        return QDialog.eventFilter(self, source, event)

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

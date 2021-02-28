import logging

from qtpy.QtCore import QObject, QPoint, QRect, Qt
from qtpy.QtGui import QMouseEvent
from qtpy.QtWidgets import QApplication, QWidget


class FramelessApplication(QApplication):
    def __init__(self, *args):
        super(FramelessApplication, self).__init__(*args)

    def notify(self, source, event) -> bool:
        if hasattr(source, "setMouseTracking"):
            source.setMouseTracking(True)
        return QApplication.notify(source, event)


class Resizer(QObject):
    """Resizer object handles frameless windows resizing events

    Note:
        Why not use eventFilter? - After closing application,
        broken reference to window may cause "underlying C/C++
        object has been deleted" error.

    Args:
        gripsize (int): Side length of grip detection area.
        dndarea (QPoint): Do Not Detect area starting from right bottom corner.
        sidegripdnd (int): Do Not Detect side length for side grips.
    """

    def __init__(self, parent=None, debug=False, gripsize=4, sidegripdnd=20, titlebarheight=50):
        super(Resizer, self).__init__(parent)
        self._debug = debug

        self._titlebarHeight = titlebarheight
        self._gripsize = gripsize
        self._sidegripdnd = sidegripdnd
        self._griprect = None
        self._hgriprect = None
        self._vgriprect = None

        self._resizing = False
        self._hor_resizing = False
        self._ver_resizing = False

        self._logger = logging.getLogger(__name__)

    def _updateGripRect(self, window):
        """Update rects for current window geometry.

        Args:
            window (QWidget): Source window
        """
        # corner grip
        self._griprect = QRect(window.width() - self._gripsize,
                               window.height() - self._gripsize,
                               self._gripsize,
                               self._gripsize)

        # right grip
        self._hgriprect = QRect(window.width() - self._gripsize,
                                self._titlebarHeight,
                                self._gripsize,
                                window.height() - self._gripsize - self._sidegripdnd - self._titlebarHeight)

        # bottom grip
        self._vgriprect = QRect(self._gripsize,
                                window.height() - self._gripsize,
                                window.width() - self._gripsize - self._sidegripdnd,
                                self._gripsize)

    def updateTitlebarHeight(self, height):
        self._titlebarHeight = height

    def handle(self, source, event, parent):
        """Handle frameless window resizing events.

        Args:
            source (QObject): Event source.
            event (QEvent): Event.
            parent (QWidget): Window to alter
        """

        try:
            self._updateGripRect(parent)
            try:
                if hasattr(source, "window") and source.window() is parent:
                    if self._debug:
                        self._logger.debug(
                            "Accepting event from: " + str(source) + "\nEvent type is: " + str(event.type()))
                    if parent.isResizingEnabled() and parent.windowState() not in (
                            Qt.WindowFullScreen, Qt.WindowMaximized):
                        # button pressed
                        if event.type() == QMouseEvent.MouseButtonPress:
                            self._updateGripRect(parent)
                            if self._griprect.contains(
                                    event.pos()) and not self._hor_resizing and not self._ver_resizing:
                                # corner grip
                                self._resizing = True

                            elif self._hgriprect.contains(
                                    event.pos()) and not self._resizing and not self._ver_resizing:
                                # right grip
                                self._hor_resizing = True

                            elif self._vgriprect.contains(
                                    event.pos()) and not self._resizing and not self._hor_resizing:
                                # bottom grip
                                self._ver_resizing = True

                        if event.type() == QMouseEvent.MouseButtonRelease:
                            # stop resizing
                            if self._resizing or self._hor_resizing or self._ver_resizing:
                                QApplication.restoreOverrideCursor()
                                self._resizing = False
                                self._hor_resizing = False
                                self._ver_resizing = False
                                QApplication.restoreOverrideCursor()
                                self._updateGripRect(parent)

                        if event.type() == QMouseEvent.MouseMove:
                            # moving
                            self._updateGripRect(parent)
                            if self._resizing and not self._hor_resizing and not self._ver_resizing:
                                if event.buttons() == Qt.LeftButton:
                                    QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
                                    parent.resize(event.x(), event.y())
                                    self._updateGripRect(parent)
                                    parent.update()
                                    QApplication.restoreOverrideCursor()

                            elif self._hor_resizing and not self._resizing and not self._ver_resizing:
                                if event.buttons() == Qt.LeftButton:
                                    QApplication.setOverrideCursor(Qt.SizeHorCursor)
                                    parent.resize(event.x(), parent.height())
                                    self._updateGripRect(parent)
                                    parent.update()
                                    QApplication.restoreOverrideCursor()

                            elif self._ver_resizing and not self._resizing and not self._hor_resizing:
                                if event.buttons() == Qt.LeftButton:
                                    QApplication.setOverrideCursor(Qt.SizeVerCursor)
                                    parent.resize(parent.width(), event.y())
                                    self._updateGripRect(parent)
                                    parent.update()
                                    QApplication.restoreOverrideCursor()

                            else:
                                if self._griprect.contains(
                                        event.pos()) and not self._hor_resizing and not self._ver_resizing:
                                    QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
                                elif self._hgriprect.contains(
                                        event.pos()) and not self._resizing and not self._ver_resizing:
                                    QApplication.setOverrideCursor(Qt.SizeHorCursor)
                                elif self._vgriprect.contains(
                                        event.pos()) and not self._resizing and not self._hor_resizing:
                                    QApplication.setOverrideCursor(Qt.SizeVerCursor)
                                else:
                                    QApplication.restoreOverrideCursor()
            except Exception as e:
                if self._debug:
                    self._logger.critical(e)

        except Exception as e:
            self._logger.critical(e)

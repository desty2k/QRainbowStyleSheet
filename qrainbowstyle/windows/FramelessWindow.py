import logging

from qtpy.QtCore import QObject, QRect, Qt, QPoint, QSize, QEvent
from qtpy.QtGui import QMouseEvent, QCursor
from qtpy.QtWidgets import QApplication, QWidget

from .base import FramelessWindowBase


class FramelessWindow(FramelessWindowBase):
    """Frameless window for non-Windows OS like Linux and Darwin.
    Reimplements features:
    - window moving
    - window resizing
    - maximize on double click on titlebar
    - snap to borders
    """

    def __init__(self, parent=None):
        super(FramelessWindow, self).__init__(parent)

        self.__titlebarHeight = 45
        self.__gripsize = 3
        self.__sideGripIgnore = 20
        self.__griprect = None
        self.__hgriprect = None
        self.__vgriprect = None

        self.__moving = False
        self.__move_offset = QPoint()

        self.__resizing = False
        self.__horizontalResizing = False
        self.__verticalResizing = False

        self.installEventFilter(self)
        self.__updateGripRect()
        self.setMouseTracking(True)

    def setMouseTracking(self, flag):
        """Recursively enables mouse tracking for all child widgets.
        This is required because eventFilter does not catch
        hover events.

        Args:
            flag (bool): Enable or disable mouse tracking.
        """
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except AttributeError:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def __updateGripRect(self):
        """Update rects for current window geometry."""
        # corner grip
        self.__griprect = QRect(self.width() - self.__gripsize,
                                self.height() - self.__gripsize,
                                self.__gripsize,
                                self.__gripsize)

        # right grip
        self.__hgriprect = QRect(self.width() - self.__gripsize,
                                 self.__titlebarHeight,
                                 self.__gripsize,
                                 self.height() - self.__gripsize - self.__sideGripIgnore - self.__titlebarHeight)

        # bottom grip
        self.__vgriprect = QRect(self.__gripsize,
                                 self.height() - self.__gripsize,
                                 self.width() - self.__gripsize - self.__sideGripIgnore,
                                 self.__gripsize)

    def eventFilter(self, widget, event: QEvent):
        """Handle frameless window events.

        Args:
            widget (QObject): Widget.
            event (QEvent): Event.
        """
        if (hasattr(widget, "window")
                and widget.window() is self):
            self.__updateGripRect()

            if (hasattr(event, "x")
                    and self.titlebar().rect().contains(self.mapFromParent(QCursor.pos()))
                    and self.titlebar().mouseOverTitlebar(event.x(), event.y())):
                # when cursor is over titlebar

                if event.type() == QMouseEvent.MouseButtonPress and event.buttons() == Qt.LeftButton:
                    # if titlebar clicked with left button
                    self.__moving = True
                    margins = self.titlebar().contentsMargins()
                    self.__move_offset = event.pos() + self.titlebar().pos() - QPoint(margins.left(), margins.top())

                elif event.type() == QMouseEvent.MouseMove and event.buttons() == Qt.LeftButton:
                    # if holding left button and moving window
                    if self.__moving:
                        if self.windowState() == Qt.WindowMaximized:
                            self.setWindowState(Qt.WindowNoState)
                            self.titlebar().on_btnRestore_clicked()
                            self.move(event.pos() - self.mapFromParent(event.pos()))
                            self.__moving = False
                        else:
                            self.move(event.globalPos() - self.__move_offset)

                elif event.type() == QMouseEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
                    # if left button released
                    self.__moving = False
                    screen = QApplication.instance().desktop().availableGeometry()
                    if event.globalY() == 0:
                        # snap to top edge
                        pass
                        self.titlebar().on_btnMaximize_clicked()

                    elif event.globalX() == 0:
                        # snap to left edge
                        self.move(QPoint(0, 0))
                        self.resize(QSize(screen.width() / 2, screen.height()))
                        self.setWindowState(Qt.WindowNoState)

                    elif event.globalX() + 1 >= screen.width():
                        # snap to right edge
                        self.move(QPoint(screen.width() / 2, 0))
                        self.resize(QSize(screen.width() / 2, screen.height()))
                        self.setWindowState(Qt.WindowNoState)

                    elif self.geometry().y() < 0:
                        # move window if top of window is outside display
                        self.move(QPoint(self.geometry().x(), 0))

                elif event.type() == QMouseEvent.MouseButtonDblClick:
                    # maximize/restore on double click
                    if self.windowState() == Qt.WindowMaximized:
                        self.setWindowState(Qt.WindowNoState)
                    elif self.windowState() == Qt.WindowNoState:
                        self.showMaximized()

            elif event.type() == QEvent.Leave and widget is self.titlebar():
                # fixes __moving remain True after clicking titlebar on border and leaving titlebar
                self.__moving = False

            elif (self.windowState() not in (Qt.WindowFullScreen, Qt.WindowMaximized)
                    and self.isResizingEnabled()):
                # when cursor is not over titlebar
                # and window is not maximized or in full screen mode

                # button pressed
                if event.type() == QMouseEvent.MouseButtonPress:
                    if self.__griprect.contains(
                            event.pos()) and not self.__horizontalResizing and not self.__verticalResizing:
                        # corner grip
                        self.__resizing = True

                    elif self.__hgriprect.contains(
                            event.pos()) and not self.__resizing and not self.__verticalResizing:
                        # right grip
                        self.__horizontalResizing = True

                    elif self.__vgriprect.contains(
                            event.pos()) and not self.__resizing and not self.__horizontalResizing:
                        # bottom grip
                        self.__verticalResizing = True

                if event.type() == QMouseEvent.MouseButtonRelease:
                    # stop resizing
                    if self.__resizing or self.__horizontalResizing or self.__verticalResizing:
                        self.__resizing = False
                        self.__horizontalResizing = False
                        self.__verticalResizing = False
                        self.setCursor(Qt.ArrowCursor)

                if event.type() == QMouseEvent.MouseMove:
                    # moving cursor while holding left button -> resize

                    if self.__resizing and not self.__horizontalResizing and not self.__verticalResizing:
                        if event.buttons() == Qt.LeftButton:
                            self.setCursor(Qt.SizeFDiagCursor)
                            self.resize(QSize(event.x(), event.y()))

                    elif self.__horizontalResizing and not self.__resizing and not self.__verticalResizing:
                        if event.buttons() == Qt.LeftButton:
                            self.setCursor(Qt.SizeHorCursor)
                            self.resize(QSize(event.x(), self.height()))

                    elif self.__verticalResizing and not self.__resizing and not self.__horizontalResizing:
                        if event.buttons() == Qt.LeftButton:
                            self.setCursor(Qt.SizeVerCursor)
                            self.resize(QSize(self.width(), event.y()))

                    else:
                        if (self.__griprect.contains(event.pos())
                                and not self.__horizontalResizing
                                and not self.__verticalResizing):
                            self.setCursor(Qt.SizeFDiagCursor)
                        elif (self.__hgriprect.contains(event.pos())
                              and not self.__resizing
                              and not self.__verticalResizing):
                            self.setCursor(Qt.SizeHorCursor)
                        elif (self.__vgriprect.contains(event.pos())
                              and not self.__resizing
                              and not self.__horizontalResizing):
                            self.setCursor(Qt.SizeVerCursor)
                        else:
                            self.setCursor(Qt.ArrowCursor)

        return super().eventFilter(widget, event)

import sys

if sys.platform == "win32":
    try:
        from PyQt5.QtWinExtras import QtWin
        import win32con
        import win32gui
        import win32api
        import ctypes.wintypes
        from ctypes.wintypes import POINT
    except Exception as e:
        raise ImportError("Could not import required library for Windows support: ".format(e))

else:
    raise Exception("Windows API is not supported on non Windows OS.")

from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QMetaObject, Slot

from .base import FramelessWindowBase


class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved", POINT),
        ("ptMaxSize", POINT),
        ("ptMaxPosition", POINT),
        ("ptMinTrackSize", POINT),
        ("ptMaxTrackSize", POINT),
    ]


class FramelessWindow(FramelessWindowBase):
    """Frameless window for Windows OS.

    Available features:
        - window moving
        - window resizing
        - maximize on double click on titlebar
        - native snap to borders
        - Aero shake
        - window shadow
    """

    def __init__(self, parent=None):
        super(FramelessWindow, self).__init__(parent)
        self.__rect = QApplication.instance().desktop().availableGeometry(self)

        self.__titlebarHeight = 45
        self.__borderWidth = 3

        self.hwnd = None

        if QtWin.isCompositionEnabled():
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)
        QMetaObject.connectSlotsByName(self)

    def setWindowFlags(self, flags):
        """Sets window flags. Window must be
        re-shown after calling this method.

        Args:
            flags (WindowFlags): Window flags.
        """
        self.hwnd = None
        super().setWindowFlags(flags)
        self.show()

    def show(self):
        """Shows the window."""
        if not self.hwnd:
            self.__setStyle()
        super().show()

    def showNormal(self):
        """Shows the window as normal, i.e. neither maximized, minimized, nor fullscreen."""
        if not self.hwnd:
            self.__setStyle()
        super().showNormal()

    def showMaximized(self):
        """Shows the window as maximized."""
        if not self.hwnd:
            self.__setStyle()
        super().showMaximized()

    def showMinimized(self):
        """Shows the window as minimized."""
        if not self.hwnd:
            self.__setStyle()
        super().showMinimized()

    def showFullScreen(self):
        """Shows the window as fullscreen."""
        if not self.hwnd:
            self.__setStyle()
        super().showFullScreen()

    def showWindowShadow(self, value: bool):
        """Show or hide window shadow.

        Args:
            value (bool): Enable or disable window shadow
        """
        if value:
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.extendFrameIntoClientArea(self, 0, 0, 0, 0)

    def setResizingEnabled(self, value: bool):
        """Enable window resizing

        Args:
            value (bool): Enable or disable window resizing
        """
        self.__resizingEnabled = value

    def setEdgeSnapping(self, value: bool):
        """Enable or disable edge snapping for window.

        Args:
            value (bool): Enable or disable edge snapping.
        """
        if not self.hwnd:
            self.__setStyle()

        if value:
            style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_STYLE)
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_STYLE, style | win32con.WS_TILEDWINDOW)
        else:
            style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_STYLE)
            win32gui.SetWindowLong(
                self.hwnd, win32con.GWL_STYLE, style & ~win32con.WS_OVERLAPPEDWINDOW | win32con.WS_POPUPWINDOW)

    def nativeEvent(self, eventType, message):
        """Handle frameless window native events.

        Args:
            eventType (QByteArray): Event type.
            message (int): Message.
        """
        retval, result = super().nativeEvent(eventType, message)
        if eventType == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(int(message))

            if msg.message == win32con.WM_NCCALCSIZE:
                return True, 0

            elif msg.message == win32con.WM_GETMINMAXINFO:
                info = ctypes.cast(
                    msg.lParam, ctypes.POINTER(MINMAXINFO)).contents
                info.ptMaxSize.x = self.__rect.width()
                info.ptMaxSize.y = self.__rect.height() - 1
                info.ptMaxPosition.x, info.ptMaxPosition.y = 0, 0
                return True, 0

            elif msg.message == win32con.WM_NCHITTEST:
                x = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
                y = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
                w, h = self.width(), self.height()

                lx = x < self.__borderWidth
                rx = x > w - self.__borderWidth
                ty = y < self.__borderWidth
                by = y > h - self.__borderWidth

                titleBarX = not lx and not rx
                titleBarY = not ty and y < self.__borderWidth + self.titlebar().height()

                if titleBarX and titleBarY:
                    if self.titlebar().mouseOverTitlebar(x, y):
                        return True, win32con.HTCAPTION
                    else:
                        return retval, result

                if not lx and not ty and not rx and not by:
                    return retval, result

                if self.isResizingEnabled():
                    if lx and ty:
                        return True, win32con.HTTOPLEFT
                    if rx and by:
                        return True, win32con.HTBOTTOMRIGHT
                    if rx and ty:
                        return True, win32con.HTTOPRIGHT
                    if lx and by:
                        return True, win32con.HTBOTTOMLEFT
                    if ty:
                        return True, win32con.HTTOP
                    if by:
                        return True, win32con.HTBOTTOM
                    if lx:
                        return True, win32con.HTLEFT
                    if rx:
                        return True, win32con.HTRIGHT

        return retval, result

    def __setStyle(self):
        self.hwnd = int(self.winId())
        style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_STYLE, style | win32con.WS_TILEDWINDOW)

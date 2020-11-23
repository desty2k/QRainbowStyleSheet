from qtpy import QtWidgets, QtCore, QtGui

import qdarkstyle
from .windowButtons import titleBarWindowsButton, titleBarButton


def getButtons(parent, style=None):
    if qdarkstyle.USE_DARWIN_BUTTONS:
        return {"minimize": titleBarButton(QtGui.QIcon(":/qss_icons/rc/button_darwin_minimize.png"),
                                           QtGui.QIcon(":/qss_icons/rc/button_darwin_minimize_hover.png"),
                                           parent),
                "maximize": titleBarButton(QtGui.QIcon(":/qss_icons/rc/button_darwin_maximize.png"),
                                           QtGui.QIcon(":/qss_icons/rc/button_darwin_maximize_hover.png"),
                                           parent),
                "restore": titleBarButton(QtGui.QIcon(":/qss_icons/rc/button_darwin_restore_hover.png"),
                                          QtGui.QIcon(":/qss_icons/rc/button_darwin_restore_hover.png"),
                                          parent),
                "close": titleBarButton(QtGui.QIcon(":/qss_icons/rc/button_darwin_close.png"),
                                        QtGui.QIcon(":/qss_icons/rc/button_darwin_close_hover.png"),
                                        parent)}

    else:
        return {"minimize": titleBarWindowsButton(QtGui.QIcon(":/qss_icons/rc/button_nt_minimize.png"),
                                                  QtGui.QIcon(":/qss_icons/rc/button_nt_minimize_hover.png"),
                                                  parent),
                "maximize": titleBarWindowsButton(QtGui.QIcon(":/qss_icons/rc/button_nt_maximize.png"),
                                                  QtGui.QIcon(":/qss_icons/rc/button_nt_maximize_hover.png"),
                                                  parent),
                "restore": titleBarWindowsButton(QtGui.QIcon(":/qss_icons/rc/button_nt_restore.png"),
                                                 QtGui.QIcon(":/qss_icons/rc/button_nt_restore_hover.png"),
                                                 parent),
                "close": titleBarWindowsButton(QtGui.QIcon(":/qss_icons/rc/button_nt_close.png"),
                                               QtGui.QIcon(":/qss_icons/rc/button_nt_close_hover_red.png"),
                                               parent)}


class buttonsWidget(QtWidgets.QWidget):
    """buttonsWidget documentation"""

    def __init__(self, parent):
        super(buttonsWidget, self).__init__(parent)

        self.setObjectName("buttonsWidget")
        sizepolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizepolicy)
        self.setStyleSheet("padding: 0px;")

        self.buttonsLayout = QtWidgets.QHBoxLayout(self)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setSpacing(0)
        self.buttonsLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.setLayout(self.buttonsLayout)

        btns = getButtons(self)

        self.btnMinimize = btns["minimize"]
        self.btnMaximize = btns["maximize"]
        self.btnRestore = btns["restore"]
        self.btnClose = btns["close"]

        if qdarkstyle.ALIGN_BUTTONS_LEFT:
            self.buttonsLayout.addWidget(self.btnClose)
            if not qdarkstyle.USE_DARWIN_BUTTONS:
                self.buttonsLayout.addWidget(self.btnRestore)
            self.buttonsLayout.addWidget(self.btnMaximize)
            self.buttonsLayout.addWidget(self.btnMinimize)
        else:
            self.buttonsLayout.addWidget(self.btnMinimize)
            self.buttonsLayout.addWidget(self.btnMaximize)
            if not qdarkstyle.USE_DARWIN_BUTTONS:
                self.buttonsLayout.addWidget(self.btnRestore)
            self.buttonsLayout.addWidget(self.btnClose)

        self.btnMinimize.setObjectName("btnMinimize")
        self.btnMaximize.setObjectName("btnMaximize")
        if not qdarkstyle.USE_DARWIN_BUTTONS:
            self.btnRestore.setObjectName("btnRestore")
        self.btnClose.setObjectName("btnClose")

        if qdarkstyle.USE_DARWIN_BUTTONS:
            self.buttonsLayout.setSpacing(8)

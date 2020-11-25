from qtpy.QtWidgets import QWidget, QSizePolicy, QHBoxLayout
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt

from .windowButtons import titleBarWindowsButton, titleBarButton

import qrainbowstyle


def getButtons(parent, style=None):
    if qrainbowstyle.USE_DARWIN_BUTTONS:
        return {"minimize": titleBarButton(QIcon(":/qss_icons/rc/button_darwin_minimize.png"),
                                           QIcon(":/qss_icons/rc/button_darwin_minimize_hover.png"),
                                           parent),
                "maximize": titleBarButton(QIcon(":/qss_icons/rc/button_darwin_maximize.png"),
                                           QIcon(":/qss_icons/rc/button_darwin_maximize_hover.png"),
                                           parent),
                "restore": titleBarButton(QIcon(":/qss_icons/rc/button_darwin_restore_hover.png"),
                                          QIcon(":/qss_icons/rc/button_darwin_restore_hover.png"),
                                          parent),
                "close": titleBarButton(QIcon(":/qss_icons/rc/button_darwin_close.png"),
                                        QIcon(":/qss_icons/rc/button_darwin_close_hover.png"),
                                        parent)}

    else:
        return {"minimize": titleBarWindowsButton(QIcon(":/qss_icons/rc/button_nt_minimize.png"),
                                                  QIcon(":/qss_icons/rc/button_nt_minimize_hover.png"),
                                                  parent),
                "maximize": titleBarWindowsButton(QIcon(":/qss_icons/rc/button_nt_maximize.png"),
                                                  QIcon(":/qss_icons/rc/button_nt_maximize_hover.png"),
                                                  parent),
                "restore": titleBarWindowsButton(QIcon(":/qss_icons/rc/button_nt_restore.png"),
                                                 QIcon(":/qss_icons/rc/button_nt_restore_hover.png"),
                                                 parent),
                "close": titleBarWindowsButton(QIcon(":/qss_icons/rc/button_nt_close.png"),
                                               QIcon(":/qss_icons/rc/button_nt_close_hover_red.png"),
                                               parent)}


class buttonsWidget(QWidget):
    """buttonsWidget documentation"""

    def __init__(self, parent):
        super(buttonsWidget, self).__init__(parent)

        self.setObjectName("buttonsWidget")
        sizepolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizepolicy)
        self.setStyleSheet("padding: 0px;")

        self.buttonsLayout = QHBoxLayout(self)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setSpacing(0)
        self.buttonsLayout.setAlignment(Qt.AlignVCenter)
        self.setLayout(self.buttonsLayout)

        btns = getButtons(self)

        self.btnMinimize = btns["minimize"]
        self.btnMaximize = btns["maximize"]
        self.btnRestore = btns["restore"]
        self.btnClose = btns["close"]

        if qrainbowstyle.ALIGN_BUTTONS_LEFT:
            self.buttonsLayout.addWidget(self.btnClose)
            if not qrainbowstyle.USE_DARWIN_BUTTONS:
                self.buttonsLayout.addWidget(self.btnRestore)
            self.buttonsLayout.addWidget(self.btnMaximize)
            self.buttonsLayout.addWidget(self.btnMinimize)
        else:
            self.buttonsLayout.addWidget(self.btnMinimize)
            self.buttonsLayout.addWidget(self.btnMaximize)
            if not qrainbowstyle.USE_DARWIN_BUTTONS:
                self.buttonsLayout.addWidget(self.btnRestore)
            self.buttonsLayout.addWidget(self.btnClose)

        self.btnMinimize.setObjectName("btnMinimize")
        self.btnMaximize.setObjectName("btnMaximize")
        if not qrainbowstyle.USE_DARWIN_BUTTONS:
            self.btnRestore.setObjectName("btnRestore")
        self.btnClose.setObjectName("btnClose")

        if qrainbowstyle.USE_DARWIN_BUTTONS:
            self.buttonsLayout.setSpacing(8)

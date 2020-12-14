from qtpy.QtWidgets import QWidget, QSizePolicy, QHBoxLayout
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt, QEvent

from .windowButtons import titleBarWindowsButton, titleBarButton

import qrainbowstyle


def getIcons():
    if qrainbowstyle.USE_DARWIN_BUTTONS:
        return {"minimize": {"normal": QIcon(":/qss_icons/rc/button_darwin_minimize.png"),
                             "hover": QIcon(":/qss_icons/rc/button_darwin_minimize_hover.png")},
                "maximize": {"normal": QIcon(":/qss_icons/rc/button_darwin_maximize.png"),
                             "hover": QIcon(":/qss_icons/rc/button_darwin_maximize_hover.png")},
                "restore": {"normal": QIcon(":/qss_icons/rc/button_darwin_restore_hover.png"),
                            "hover": QIcon(":/qss_icons/rc/button_darwin_restore_hover.png")},
                "close": {"normal": QIcon(":/qss_icons/rc/button_darwin_close.png"),
                          "hover": QIcon(":/qss_icons/rc/button_darwin_close_hover.png")}
                }

    else:
        return {"minimize": {"normal": QIcon(":/qss_icons/rc/button_nt_minimize.png"),
                             "hover": QIcon(":/qss_icons/rc/button_nt_minimize_hover.png")},
                "maximize": {"normal": QIcon(":/qss_icons/rc/button_nt_maximize.png"),
                             "hover": QIcon(":/qss_icons/rc/button_nt_maximize_hover.png")},
                "restore": {"normal": QIcon(":/qss_icons/rc/button_nt_restore.png"),
                            "hover": QIcon(":/qss_icons/rc/button_nt_restore_hover.png")},
                "close": {"normal": QIcon(":/qss_icons/rc/button_nt_close.png"),
                          "hover": QIcon(":/qss_icons/rc/button_nt_close_hover_red.png")}
                }


def getButtons(parent):
    """Loads titlebar buttons to dict depending on selected style (NT/Darwin)

    Args:
        parent (QWidget, required): Widget where buttons will be used.

    Returns:
        buttons (dict): Dict with close, minimize, restore and maximize buttons.
    """

    if qrainbowstyle.USE_DARWIN_BUTTONS:
        return {"minimize": titleBarButton(QIcon(":/qss_icons/rc/button_darwin_minimize.png"),
                                           QIcon(":/qss_icons/rc/button_darwin_minimize_hover.png"),
                                           parent),
                "maximize": titleBarButton(QIcon(":/qss_icons/rc/button_darwin_maximize.png"),
                                           QIcon(":/qss_icons/rc/button_darwin_maximize_hover.png"),
                                           parent),
                "restore": titleBarButton(QIcon(":/qss_icons/rc/button_darwin_restore.png"),
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
    """Widget which contains titlebar buttons"""

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
        self.buttonsLayout.setContentsMargins(5, 0, 5, 0)
        self.buttonsLayout.setSpacing(0)
        self.buttonsLayout.setAlignment(Qt.AlignVCenter)
        self.setLayout(self.buttonsLayout)

        btns = getButtons(self)

        self.btnMinimize = btns["minimize"]
        self.btnMaximize = btns["maximize"]
        self.btnRestore = btns["restore"]
        self.btnClose = btns["close"]

        if qrainbowstyle.ALIGN_BUTTONS_LEFT:
            # reversed order
            self.buttonsLayout.addWidget(self.btnClose)
            if not qrainbowstyle.USE_DARWIN_BUTTONS:
                self.buttonsLayout.addWidget(self.btnRestore)
            self.buttonsLayout.addWidget(self.btnMaximize)
            self.buttonsLayout.addWidget(self.btnMinimize)
        else:
            # normal order
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

    def _update_buttons_icons(self):
        icons_dict = getIcons()
        self.btnMinimize.setIcons(icons_dict["minimize"]["normal"], icons_dict["minimize"]["hover"])
        self.btnMaximize.setIcons(icons_dict["maximize"]["normal"], icons_dict["maximize"]["hover"])
        self.btnRestore.setIcons(icons_dict["restore"]["normal"], icons_dict["restore"]["hover"])
        self.btnClose.setIcons(icons_dict["close"]["normal"], icons_dict["close"]["hover"])

        self.btnMinimize.leaveEvent(None)
        self.btnMaximize.leaveEvent(None)
        self.btnRestore.leaveEvent(None)
        self.btnClose.leaveEvent(None)

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.StyleChange:
            if hasattr(self, "btnMinimize") and hasattr(self, "btnMaximize") and hasattr(self, "btnRestore") and hasattr(self, "btnClose"):
                self._update_buttons_icons()

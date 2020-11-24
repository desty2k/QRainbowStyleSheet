from qtpy import QtWidgets, QtCore, QtGui

from .titlebar import Titlebar


class FramelessDialog(QtWidgets.QDialog):
    closed = QtCore.Signal()
    """FramelessDialog documentation"""

    def __init__(self, parent=None):
        super(FramelessDialog, self).__init__(parent)
        self.resize(300, 500)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(11, 5, 11, 11)
        self.bar = Titlebar(self)
        self.layout.addWidget(self.bar)

        self.closed = self.bar.terminate.clicked
        self.closed.connect(self.close)


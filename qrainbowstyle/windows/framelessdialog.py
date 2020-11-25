from qtpy.QtCore import Signal, Qt
from qtpy.QtWidgets import QDialog, QVBoxLayout

from .titlebar import Titlebar


class FramelessDialog(QDialog):
    closed = Signal()
    """FramelessDialog documentation"""

    def __init__(self, parent=None):
        super(FramelessDialog, self).__init__(parent)
        self.resize(300, 500)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(11, 5, 11, 11)
        self.bar = Titlebar(self)
        self.layout.addWidget(self.bar)

        self.closed = self.bar.terminate.clicked
        self.closed.connect(self.close)

from qtpy.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton
from qtpy.QtCore import Qt, QSize, qInstallMessageHandler

import os
import sys
import random

import qrainbowstyle
from qrainbowstyle.widgets import GoogleMapsView
from qrainbowstyle.windows import FramelessMainWindow
from qrainbowstyle.extras import OutputLogger, qt_message_handler
from qrainbowstyle.utils import setStylesheetOnQApp


def _change_style():
    styles = qrainbowstyle.get_available_styles()
    setStylesheetOnQApp(qrainbowstyle.get_available_styles()[random.randint(0, len(styles)) - 1])


class mainWidget(QWidget):
    """mainWidget documentation"""

    def __init__(self, parent=None):
        super(mainWidget, self).__init__(parent)
        self.setMinimumSize(QSize(1000, 600))

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.map = GoogleMapsView(self, "API_KEY")
        self.map.loadFinished.connect(self.test)
        self._layout.addWidget(self.map)

        self.btn = QPushButton(self)
        self.btn.setText("Change style")
        self.btn.clicked.connect(_change_style)
        self._layout.addWidget(self.btn)

    def test(self):
        poly = []
        for i in range(1, 10):
            import random
            x = random.randint(-80, 80)
            y = random.randint(-179, 179)
            self.map.addMarker(i, x, y)
            poly.append({"lat": x, "lng": y})

        self.map.addPolyline("0", poly)


def main():
    logmodule = qrainbowstyle.extras.OutputLogger()
    qInstallMessageHandler(qt_message_handler)

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet())
    qrainbowstyle.set_app_icon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "github_logo.png"))
    qrainbowstyle.set_app_name("GoogleMapsWidget Example")

    win = FramelessMainWindow()

    widget = mainWidget(win)

    win.addContentWidget(widget)
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
